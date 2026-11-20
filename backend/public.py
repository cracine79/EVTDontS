"""Server-rendered public pages (landing, video list, video pages), sitemap/robots,
the SPA mount at /app, and redirects from the old root-level SPA URLs."""
import json
import os
import re
from html import unescape
from urllib.parse import urlparse

from flask import (Blueprint, Response, abort, current_app, redirect, render_template,
                   request, send_from_directory, url_for)
from sqlalchemy import text

from exts import db
from models import Chapter, Unit

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


@public_bp.app_context_processor
def inject_globals():
    return {
        'site_url': current_app.config.get('SITE_URL', 'https://www.economicsvideos.com'),
        'spa_css': _spa_css(),
        'youtube_id': youtube_id,
    }


# ---------- public pages ----------

@public_bp.route('/')
def landing():
    return render_template('landing.html')


@public_bp.route('/videos')
def videos():
    q = request.args.get('q', '').strip()
    results = search_chapters(q) if q else None
    return render_template('videos.html', units=units_with_chapters(), q=q, results=results,
                           plain_text=plain_text)


@public_bp.route('/videos/<slug>')
def video(slug):
    if slug in SLUG_REDIRECTS:
        return redirect(url_for('public.video', slug=SLUG_REDIRECTS[slug]), 301)

    chapter = Chapter.query.filter_by(slug=slug).first()
    if not chapter:
        abort(404)

    ordered = Chapter.query.order_by(Chapter.order).all()
    idx = next(i for i, c in enumerate(ordered) if c.id == chapter.id)
    prev_ch = ordered[idx - 1] if idx > 0 else None
    next_ch = ordered[idx + 1] if idx + 1 < len(ordered) else None

    return render_template(
        'video.html',
        chapter=chapter,
        yt=youtube_id(chapter.video_url),
        units=units_with_chapters(),
        prev_ch=prev_ch,
        next_ch=next_ch,
        video_blurb=clean_blurb(chapter.video_blurb),
        quiz_blurb=clean_blurb(chapter.quiz_blurb),
        description=plain_text(chapter.video_blurb, 155),
        short_name=chapter.name.split(' ', 1)[-1],
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
        return send_from_directory(BUILD_DIR, path)
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
