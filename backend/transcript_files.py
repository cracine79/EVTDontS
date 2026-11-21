"""Hand-editable transcript files: backend/seed_files/transcripts/<number>-<slug>.txt

File format:
    STATUS: draft            <- change to "done" when cleaned up; only "done" ones show on the site
    # comment lines start with "#" and are ignored
    (blank line)
    First paragraph...

    Second paragraph...       <- paragraphs are separated by a blank line
"""
import os
import re

TRANSCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_files', 'transcripts')


def transcript_path(name, slug):
    number = (name or '').split(' ', 1)[0]
    prefix = number if re.match(r'^[\d.]+[a-z]?$', number) else 'x'
    return os.path.join(TRANSCRIPT_DIR, f'{prefix}-{slug}.txt')


def write_draft(name, slug, text):
    """Create the file for a transcript if it doesn't exist yet. Never overwrites your edits."""
    path = transcript_path(name, slug)
    if os.path.exists(path) or not text:
        return False
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    with open(path, 'w') as f:
        f.write('STATUS: draft\n')
        f.write(f'# {name}\n')
        f.write('# Clean this up, then change the first line to "STATUS: done" so it shows on the site.\n')
        f.write('# Separate paragraphs with a blank line. Lines starting with "#" are ignored.\n\n')
        f.write(text.strip() + '\n')
    return True


def read_transcript(name, slug):
    """(status, text) from the file, or (None, None) if there is no file."""
    path = transcript_path(name, slug)
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        lines = f.read().splitlines()
    status = 'draft'
    if lines and lines[0].strip().upper().startswith('STATUS:'):
        status = lines[0].split(':', 1)[1].strip().lower()
        lines = lines[1:]
    body = '\n'.join(l for l in lines if not l.lstrip().startswith('#')).strip()
    paragraphs = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', body)]
    return status, '\n\n'.join(p for p in paragraphs if p)
