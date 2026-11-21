"""Dev-only: pull upload date, duration and transcript for every chapter's YouTube video
into seed_files/video_metadata.json, which you can review/edit and commit.
Then load it into a database with seed_video_metadata.py.

    pip install youtube-transcript-api        # dev only, not in requirements.txt
    python fetch_video_metadata.py            # fill in anything missing; never overwrites
    python fetch_video_metadata.py --rebuild  # rebuild transcripts from the raw caption cache
                                              # (overwrites hand edits in the JSON)
    python fetch_video_metadata.py --skip-transcripts   # dates/durations/chapters only

Raw captions are cached in seed_files/transcripts_raw/ so cleanup can be re-run without
calling YouTube (which rate-limits/blocks repeated transcript downloads).

Each transcript also gets a hand-editable file in seed_files/transcripts/ (created once, never
overwritten). Edit it, change its first line to "STATUS: done", and run seed_video_metadata.py;
only "done" transcripts are shown on the site.
"""
import json
import os
import re
import sys
import urllib.request

from youtube_transcript_api import YouTubeTranscriptApi

from config import DevConfig
from main import create_app
from models import Chapter
from public import youtube_id
from transcript_files import write_draft

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'seed_files', 'video_metadata.json')
RAW_DIR = os.path.join(HERE, 'seed_files', 'transcripts_raw')

# Auto-caption mistakes that recur in the intros ("I'm Mr. Racine, welcome to today's episode of
# Economics Videos That Don't Suck"); other proper nouns (Mr. Big, Mr. White...) are left alone
REPLACEMENTS = [
    (r"\bI'm Mr\.? [A-Za-z]+", "I'm Mr. Racine"),
    (r"\bMr\.? Racine\b", "Mr. Racine"),
]

# The channel name is sung over music in the intro, so captions drop or mishear it
# ("economics foreign", "look at this", "Economics with Youssef and Don't do songs").
# After "today's episode of", swallow words from this list only, then insert the real name.
INTRO_MISHEARD = {
    "a", "economics", "economic", "vide", "videos", "with", "youssef", "yo", "you", "that's",
    "dope", "and", "don't", "do", "songs", "song", "son", "that", "suck", "sucks", "reviews", "review",
    "class", "notes", "at", "foreign", "math", "screaming",
}
# Multi-word mishearings that contain everyday words ("this", "the") we can't swallow on their own
INTRO_MISHEARD_PHRASES = [['look', 'at', 'this'], ['go', 'to', 'the', 'song']]
INTRO = re.compile(r"(today's episode of)((?:\s+[\w']+)*)", re.IGNORECASE)


def fix_intro(text):
    def repl(m):
        words = m.group(2).split()
        eaten, progress = 0, True
        while progress and eaten < min(len(words), 8):
            progress = False
            lowered = [w.lower().strip(".,!?") for w in words[eaten:eaten + 4]]
            for phrase in INTRO_MISHEARD_PHRASES:
                if lowered[:len(phrase)] == phrase:
                    eaten += len(phrase)
                    progress = True
                    break
            else:
                if lowered and lowered[0] in INTRO_MISHEARD:
                    eaten += 1
                    progress = True
        rest = ' '.join(words[eaten:])
        return "today's episode of Economics Videos That Don't Suck" + (f' {rest}' if rest else '')
    return INTRO.sub(repl, text, count=1)

NOISE = re.compile(r"\[[A-Za-z _]+\]|>>")
FILLERS = re.compile(r"\b(?:uh|um|uhm|erm)\b,?\s*", re.IGNORECASE)
PARAGRAPH_SECONDS = 45
MAX_PARAGRAPH_SECONDS = 75  # older captions have no punctuation to break on


TIMESTAMP_LINE = re.compile(r'^\s*\(?((?:\d{1,2}:)?\d{1,2}:\d{2})\)?\s*[-–:|]?\s*(.+?)\s*$')


def to_seconds(stamp):
    secs = 0
    for part in stamp.split(':'):
        secs = secs * 60 + int(part)
    return secs


def description_chapters(description):
    """'0:42 Price Floors Introduced' lines -> [{'start': 42, 'label': 'Price Floors Introduced'}]"""
    chapters, seen = [], set()
    for line in description.splitlines():
        m = TIMESTAMP_LINE.match(line)
        if not m:
            continue
        start = to_seconds(m.group(1))
        label = re.sub(r'\s+', ' ', re.sub(r'^\d+\.\s+', '', m.group(2))).strip()
        if start in seen and chapters and chapters[-1]['start'] == start:
            # "7:08 Impact of Minimum Wage" followed by "7:08 1. Unemployment": keep the more specific one
            chapters[-1]['label'] = label
            continue
        seen.add(start)
        chapters.append({'start': start, 'label': label})
    return chapters


def watch_page_info(video_id):
    req = urllib.request.Request(f'https://www.youtube.com/watch?v={video_id}',
                                 headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US'})
    html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
    date = re.search(r'"publishDate":"([^"]+)"', html)
    length = re.search(r'"lengthSeconds":"(\d+)"', html)
    desc = re.search(r'"shortDescription":("(?:[^"\\]|\\.)*")', html)
    description = json.loads(desc.group(1)) if desc else ''
    return {
        'upload_date': date.group(1) if date else None,
        'duration_seconds': int(length.group(1)) if length else None,
        'chapters': description_chapters(description),
    }


def clean(text):
    """Applied to whole paragraphs: YouTube splits phrases across caption fragments."""
    text = NOISE.sub(' ', text)
    text = FILLERS.sub('', text)
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    text = fix_intro(text)
    return re.sub(r'\s+', ' ', text).strip()


def raw_captions(video_id):
    """[{text, start}] from the local cache, downloading (and caching) if needed."""
    path = os.path.join(RAW_DIR, f'{video_id}.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    snippets = [{'text': s.text, 'start': s.start}
                for s in YouTubeTranscriptApi().fetch(video_id, languages=['en'])]
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(snippets, f, ensure_ascii=False)
    return snippets


def transcript_paragraphs(snippets):
    paragraphs, current, start = [], [], None
    for s in snippets:
        text = re.sub(r'\s+', ' ', NOISE.sub(' ', s['text'])).strip()
        if not text:
            continue
        if start is None:
            start = s['start']
        current.append(text)
        elapsed = s['start'] - start
        if (elapsed >= PARAGRAPH_SECONDS and re.search(r'[.?!]["”]?$', text)) or elapsed >= MAX_PARAGRAPH_SECONDS:
            paragraphs.append(' '.join(current))
            current, start = [], None
    if current:
        paragraphs.append(' '.join(current))
    paragraphs = [clean(p) for p in paragraphs]
    return '\n\n'.join(p[:1].upper() + p[1:] for p in paragraphs if p)


def main():
    rebuild = '--rebuild' in sys.argv
    skip_transcripts = '--skip-transcripts' in sys.argv
    data = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            data = json.load(f)

    app = create_app(DevConfig)
    with app.app_context():
        chapters = Chapter.query.order_by(Chapter.order).all()

    for ch in chapters:
        vid = youtube_id(ch.video_url)
        if not vid or not ch.slug:
            continue
        entry = data.setdefault(ch.slug, {})
        entry.update({'name': ch.name, 'video_id': vid})

        if not entry.get('upload_date') or not entry.get('duration_seconds') or 'chapters' not in entry:
            try:
                info = watch_page_info(vid)
                for key, value in info.items():
                    if value or key not in entry:
                        entry[key] = value
            except Exception as e:
                print(f'  ! {ch.name}: could not read watch page ({e})')

        if not skip_transcripts and (rebuild or not entry.get('transcript')):
            try:
                entry['transcript'] = transcript_paragraphs(raw_captions(vid))
            except Exception as e:
                # Keep whatever transcript we already had
                print(f'  ! {ch.name}: no transcript ({type(e).__name__})')
                entry.setdefault('transcript', None)

        if entry.get('transcript') and write_draft(ch.name, ch.slug, entry['transcript']):
            print(f'  + created transcript file for {ch.name} (STATUS: draft)')

        print(f"{ch.name}: {entry.get('upload_date')}, {entry.get('duration_seconds')}s, "
              f"{len(entry.get('chapters') or [])} key moments, {len(entry.get('transcript') or '')} chars")

    with open(OUT, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(data)} chapters to {OUT}')


if __name__ == '__main__':
    main()
