"""Server-rendered public pages (landing, video list, video pages), sitemap/robots,
the SPA mount at /app, and redirects from the old root-level SPA URLs."""
import json
import os
import re
from html import unescape
from urllib.parse import quote, urlparse

from flask import (Blueprint, Response, abort, current_app, redirect, render_template,
                   request, send_from_directory, url_for)
from sqlalchemy import text

from exts import db
from datetime import datetime, timedelta, timezone

from models import Chapter, Question, QuestionTopic, Unit
from quiz import chapter_quiz_size

public_bp = Blueprint('public', __name__)

BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'build')

# First path segments of SPA routes that used to live at the site root.
# Old links/bookmarks/emails to these are redirected to /app/<same path>.
LEGACY_SPA_ROUTES = {
    'userhome', 'video', 'quiz', 'results', 'rqresults', 'getstarted', 'freequiz',
    'quizgenerator', 'whoops', 'updateunits', 'finishpage', 'finishunit', 'uqresults',
    'userlessresults', 'retrievedata', 'reset-password', 'privacypolicy',
    'termsofservice', 'aboutus', 'searchresults', 'contactus', 'messagesent',
}

# Slugs that were renamed; old URLs 301 to the new slug.
SLUG_REDIRECTS = {'price ceilings': 'price-ceilings'}


# ---------- helpers ----------

_manifest_cache = None


def _spa_css():
    """CSS files from the Vite build, so templates share the SPA's Tailwind styles."""
    global _manifest_cache
    if _manifest_cache is None or current_app.debug:
        try:
            with open(os.path.join(BUILD_DIR, 'manifest.json')) as f:
                manifest = json.load(f)
            _manifest_cache = ['/app/' + css for css in manifest.get('index.html', {}).get('css', [])]
        except (OSError, ValueError):
            current_app.logger.warning('Vite manifest not found; run `npm run build` in frontend2')
            _manifest_cache = []
    return _manifest_cache


def youtube_id(video_url):
    if not video_url:
        return None
    parsed = urlparse(video_url)
    if parsed.netloc.endswith('youtu.be'):
        return parsed.path.strip('/') or None
    match = re.search(r'/embed/([\w-]+)', parsed.path)
    return match.group(1) if match else None


def plain_text(html, limit=None):
    """Strip tags/whitespace from a blurb for meta descriptions."""
    if not html:
        return ''
    txt = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', html))).strip()
    if limit and len(txt) > limit:
        txt = txt[:limit].rsplit(' ', 1)[0].rstrip(',;:.') + '…'
    return txt


def iso_duration(seconds):
    """823 -> 'PT13M43S' (ISO 8601, as schema.org expects)."""
    if not seconds:
        return None
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return 'PT' + (f'{h}H' if h else '') + (f'{m}M' if m else '') + f'{s}S'


def embed_autoplay_url(video_url):
    sep = '&' if '?' in video_url else '?'
    return f'{video_url}{sep}autoplay=1'


def clean_blurb(blurb):
    # Some seeded blurbs used "/n" where a newline was intended
    return (blurb or '').replace('/n', '\n')


def units_with_chapters():
    """[(unit, [chapters ordered])] for units that have at least one chapter."""
    chapters = Chapter.query.order_by(Chapter.order).all()
    units = {u.id: u for u in Unit.query.all()}
    grouped = {}
    for ch in chapters:
        grouped.setdefault(ch.unit_id, []).append(ch)
    return [(units[uid], chs) for uid, chs in sorted(grouped.items()) if uid in units]


# ---------- unit colors & library data ----------

# Unit number -> (color, text color on it, lighter tint for text on the dark background)
UNIT_THEME = {
    1: ('#FFC93C', '#111', None),
    2: ('#C6E83A', '#111', None),
    3: ('#FF6FAE', '#111', None),
    4: ('#4CC2F5', '#111', None),
    5: ('#FF8A3D', '#111', None),
    6: ('#9B6BFF', '#fff', '#B89AFF'),
    7: ('#3DDBB5', '#111', None),
    8: ('#3B5BDB', '#fff', '#8EA2FF'),
}
# Micro units that don't have videos yet; shown as "coming soon" until a unit with that number exists
UPCOMING_UNITS = {7: 'Consumer Theory', 8: 'Factor Markets'}
NEW_UNIT_DAYS = 120  # a unit is tagged NEW if its first video is this recent


def unit_number(unit):
    m = re.match(r'\s*Unit\s+(\d+)', unit.name or '')
    return int(m.group(1)) if m else unit.id


def unit_title(name):
    return re.sub(r'^\s*Unit\s+\d+\s*:\s*', '', name or '')


def theme(number):
    color, text_color, light = UNIT_THEME.get(number, ('#7fd3e6', '#111', None))
    return {'color': color, 'text': text_color, 'light': light or color}


def mmss(seconds):
    if not seconds:
        return None
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def hours_label(seconds):
    if not seconds:
        return None
    minutes = round(seconds / 60)
    if minutes < 60:
        return f'{minutes} min'
    h, m = divmod(minutes, 60)
    return f'{h} hr {m} min' if m else f'{h} hr'


def first_sentence(html, limit=120):
    txt = plain_text(clean_blurb(html))
    m = re.match(r'(.+?[.!?])(\s|$)', txt)
    sentence = m.group(1) if m else txt
    return plain_text(sentence, limit)


def quiz_counts():
    """{chapter_id: number of questions in that chapter's practice quiz} (the quiz's size, not the question bank)."""
    rows = (db.session.query(QuestionTopic.chapter_id, QuestionTopic.id, db.func.count(Question.id))
            .join(Question, Question.topic_id == QuestionTopic.id)
            .group_by(QuestionTopic.chapter_id, QuestionTopic.id).all())
    per_chapter = {}
    for chapter_id, _, count in rows:
        per_chapter.setdefault(chapter_id, []).append(count)
    return {chapter_id: chapter_quiz_size(counts) for chapter_id, counts in per_chapter.items()}


def chapter_card(ch, counts=None):
    num, _, title = (ch.name or '').partition(' ')
    return {
        'chapter': ch,
        'num': num if title else '',
        'title': title or ch.name,
        'slug': ch.slug,
        'yt': youtube_id(ch.video_url),
        'duration': mmss(ch.video_duration_seconds),
        'teaser': first_sentence(ch.video_blurb),
        'quiz_count': (counts or {}).get(ch.id, 0),
    }


def library():
    """Units in display order, each with its theme and chapter cards; includes coming-soon units."""
    counts = quiz_counts()
    now = datetime.now(timezone.utc)
    out, numbers = [], set()
    for unit, chapters in units_with_chapters():
        number = unit_number(unit)
        numbers.add(number)
        dates = [c.video_upload_date for c in chapters if c.video_upload_date]
        first = min(dates) if dates else None
        if first is not None and first.tzinfo is None:
            first = first.replace(tzinfo=timezone.utc)
        out.append({
            'number': number,
            'title': unit_title(unit.name),
            'unit_id': unit.id,
            'cards': [chapter_card(c, counts) for c in chapters],
            'video_count': len(chapters),
            'length': hours_label(sum(c.video_duration_seconds or 0 for c in chapters)),
            'is_new': bool(first and now - first < timedelta(days=NEW_UNIT_DAYS)),
            'coming_soon': False,
            **theme(number),
        })
    for number, title in UPCOMING_UNITS.items():
        if number not in numbers:
            out.append({'number': number, 'title': title, 'unit_id': None, 'cards': [], 'video_count': 0,
                        'length': None, 'is_new': False, 'coming_soon': True, **theme(number)})
    return sorted(out, key=lambda u: u['number'])


def search_chapters(q):
    words = re.findall(r'\w+', q)
    if not words:
        return []
    terms = ' | '.join(words)
    tsquery = text("to_tsquery('english', :terms)")
    rows = (db.session.query(Chapter, db.func.ts_rank(Chapter.search_vector, tsquery).label('rank'))
            .filter(Chapter.search_vector.op('@@')(tsquery))
            .params(terms=terms).order_by(db.desc('rank')).all())
    return [ch for ch, _ in rows]


# Other domains attached to the Heroku app; they 301 to the same path on SITE_URL.
REDIRECT_HOSTS = {'www.evtds.com', 'evtds.com', 'www.economaniacs.com', 'economaniacs.com'}


@public_bp.before_app_request
def redirect_to_canonical_host():
    # Only GET/HEAD: redirecting API writes (POST/PATCH) would drop their bodies
    if request.method in ('GET', 'HEAD') and request.host.split(':')[0].lower() in REDIRECT_HOSTS:
        target = current_app.config['SITE_URL'] + request.full_path.rstrip('?')
        return redirect(target, 301)


def auth_url(mode):
    """/app/login or /app/signup, returning to the current page if the visitor closes the box."""
    here = request.full_path.rstrip('?') if request else '/'
    return f'/app/{mode}?next={quote(here, safe="/")}'


@public_bp.app_context_processor
def inject_globals():
    return {
        'auth_url': auth_url,
        'site_url': current_app.config.get('SITE_URL', 'https://www.economicsvideos.com'),
        'spa_css': _spa_css(),
        'youtube_id': youtube_id,
    }


# ---------- public pages ----------

@public_bp.route('/')
def landing():
    units = library()
    return render_template('landing.html', units=units,
                           total_videos=sum(u['video_count'] for u in units),
                           live_units=sum(1 for u in units if not u['coming_soon']))


@public_bp.route('/videos')
def videos():
    q = request.args.get('q', '').strip()
    results = search_chapters(q) if q else None
    units = library()
    counts = quiz_counts() if results else {}
    return render_template('videos.html', units=units, q=q,
                           results=[chapter_card(c, counts) for c in results] if results else results,
                           total_videos=sum(u['video_count'] for u in units),
                           live_units=sum(1 for u in units if not u['coming_soon']))


@public_bp.route('/videos/<slug>')
def video(slug):
    if slug in SLUG_REDIRECTS:
        return redirect(url_for('public.video', slug=SLUG_REDIRECTS[slug]), 301)

    chapter = Chapter.query.filter_by(slug=slug).first()
    if not chapter:
        abort(404)

    units = library()
    ordered = [card for u in units for card in u['cards']]
    idx = next(i for i, c in enumerate(ordered) if c['chapter'].id == chapter.id)
    current = ordered[idx]
    prev_card = ordered[idx - 1] if idx > 0 else None
    next_card = ordered[idx + 1] if idx + 1 < len(ordered) else None
    unit = next(u for u in units if any(c['chapter'].id == chapter.id for c in u['cards']))
    unit_of = {c['chapter'].id: u for u in units for c in u['cards']}

    yt = current['yt']
    description = plain_text(chapter.video_blurb, 155)
    transcript_paragraphs = [p for p in (chapter.transcript or '').split('\n\n') if p.strip()]
    key_moments = [{'start': m['start'], 'label': m['label'], 'time': mmss(m['start']) or '0:00'}
                   for m in (chapter.video_chapters or []) if 'start' in m and m.get('label')]
    base = current_app.config['SITE_URL']

    video_ld = None
    if yt:
        clips = []
        for i, m in enumerate(key_moments):
            end = key_moments[i + 1]['start'] if i + 1 < len(key_moments) else chapter.video_duration_seconds
            clips.append({'@type': 'Clip', 'name': m['label'], 'startOffset': m['start'],
                          **({'endOffset': end} if end else {}),
                          'url': f'https://www.youtube.com/watch?v={yt}&t={m["start"]}s'})
        video_ld = {k: v for k, v in {
            '@context': 'https://schema.org',
            '@type': 'VideoObject',
            'name': chapter.name,
            'description': description,
            'thumbnailUrl': [f'https://i.ytimg.com/vi/{yt}/hqdefault.jpg'],  # every video has this size
            'embedUrl': f'https://www.youtube.com/embed/{yt}',
            'contentUrl': f'https://www.youtube.com/watch?v={yt}',
            'url': base + request.path,
            'uploadDate': chapter.video_upload_date.isoformat() if chapter.video_upload_date else None,
            'duration': iso_duration(chapter.video_duration_seconds),
            'transcript': '\n\n'.join(transcript_paragraphs) or None,
            'hasPart': clips or None,
            'inLanguage': 'en',
            'isFamilyFriendly': True,
            'publisher': {'@type': 'Organization', 'name': "Economics Videos That Don't Suck", 'url': base + '/'},
        }.items() if v is not None}

    return render_template(
        'video.html',
        chapter=chapter,
        card=current,
        unit=unit,
        units=units,
        unit_of=unit_of,
        prev_card=prev_card,
        next_card=next_card,
        video_ld=video_ld,
        yt=yt,
        video_blurb=clean_blurb(chapter.video_blurb),
        embed_url=embed_autoplay_url(chapter.video_url),
        upload_label=(chapter.video_upload_date.strftime('%B %-d, %Y') if chapter.video_upload_date else None),
        key_moments=key_moments,
        transcript_paragraphs=transcript_paragraphs,
        description=description,
        short_name=current['title'],
    )


# ---------- SEO files ----------

@public_bp.route('/sitemap.xml')
def sitemap():
    base = current_app.config['SITE_URL']
    urls = [f'{base}/', f'{base}/videos']
    urls += [f"{base}{url_for('public.video', slug=c.slug)}"
             for c in Chapter.query.order_by(Chapter.order).all() if c.slug]
    xml = render_template('sitemap.xml', urls=urls)
    return Response(xml, mimetype='application/xml')


@public_bp.route('/robots.txt')
def robots():
    base = current_app.config['SITE_URL']
    body = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /app/\n'
        'Disallow: /api/\n'
        '\n'
        f'Sitemap: {base}/sitemap.xml\n'
    )
    return Response(body, mimetype='text/plain')


# ---------- SPA (logged-in student area) ----------

def _spa_index():
    resp = send_from_directory(BUILD_DIR, 'index.html')
    resp.headers['Cache-Control'] = 'no-cache'
    return resp


@public_bp.route('/app')
def spa_root():
    return redirect('/app/' + (f'?{request.query_string.decode()}' if request.query_string else ''))


@public_bp.route('/app/')
@public_bp.route('/app/<path:path>')
def spa(path=''):
    if path and os.path.isfile(os.path.join(BUILD_DIR, path)):
        # assets/ files have a content hash in their name, so they can be cached "forever"
        max_age = 31536000 if path.startswith('assets/') else 86400
        resp = send_from_directory(BUILD_DIR, path, max_age=max_age)
        if path.startswith('assets/'):
            resp.headers['Cache-Control'] = f'public, max-age={max_age}, immutable'
        return resp
    return _spa_index()


# ---------- redirects from old URLs ----------

@public_bp.route('/video-library')
@public_bp.route('/video-library/')
def old_video_library():
    return redirect(url_for('public.videos'), 301)


@public_bp.route('/video-library/<slug>')
def old_video_library_video(slug):
    return redirect(url_for('public.video', slug=SLUG_REDIRECTS.get(slug, slug)), 301)


@public_bp.route('/<path:path>')
def catch_all(path):
    first = path.split('/', 1)[0]
    if first == 'api':
        abort(404)
    if first.lower() in LEGACY_SPA_ROUTES:
        target = '/app/' + path
        if request.query_string:
            target += '?' + request.query_string.decode()
        return redirect(target, 301)
    # Files from the build at the old root location (favicon, cached asset URLs)
    if os.path.isfile(os.path.join(BUILD_DIR, path)):
        return send_from_directory(BUILD_DIR, path)
    abort(404)


@public_bp.app_errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return {'message': 'Not found'}, 404
    return render_template('404.html'), 404
