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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'seed_files', 'video_metadata.json')
RAW_DIR = os.path.join(HERE, 'seed_files', 'transcripts_raw')

# Auto-caption mistakes that recur in the intros ("I'm Mr. Racine, welcome to today's episode of
# Economics Videos That Don't Suck"); other proper nouns (Mr. Big, Mr. White...) are left alone
REPLACEMENTS = [
    (r"\bI'm Mr\.? [A-Za-z]+", "I'm Mr. Racine"),
    (r"\bMr\.? Racine\b", "Mr. Racine"),
    (r"(?i)(today's episode of) (?:a )?economics(?: [\w']+){0,4}? (?:suck|songs?|son|notes)\b",
     r"\1 Economics Videos That Don't Suck"),
]
NOISE = re.compile(r"\[[A-Za-z _]+\]|>>")
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
    text = NOISE.sub(' ', text)
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
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
        text = clean(s['text'])
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
    return '\n\n'.join(paragraphs)


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

        print(f"{ch.name}: {entry.get('upload_date')}, {entry.get('duration_seconds')}s, "
              f"{len(entry.get('chapters') or [])} key moments, {len(entry.get('transcript') or '')} chars")

    with open(OUT, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(data)} chapters to {OUT}')


if __name__ == '__main__':
    main()
