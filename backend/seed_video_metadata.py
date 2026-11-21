"""Load seed_files/video_metadata.json (upload dates, durations, key moments, transcripts) into the chapter
table, matched by slug. Safe to re-run: it only fills in or updates values present in the JSON.

    python seed_video_metadata.py                          # locally, from backend/
    heroku run python backend/seed_video_metadata.py       # production
"""
import json
import os
from datetime import datetime

from config import ProdConfig
from exts import db
from main import create_app
from models import Chapter
from transcript_files import read_transcript

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_files', 'video_metadata.json')

app = create_app(ProdConfig)


def main():
    with open(SOURCE) as f:
        data = json.load(f)

    with app.app_context():
        updated, published, missing = 0, 0, []
        for slug, entry in data.items():
            chapter = Chapter.query.filter_by(slug=slug).first()
            if not chapter:
                missing.append(slug)
                continue
            if entry.get('upload_date'):
                chapter.video_upload_date = datetime.fromisoformat(entry['upload_date'])
            if entry.get('duration_seconds'):
                chapter.video_duration_seconds = entry['duration_seconds']
            if entry.get('chapters'):
                chapter.video_chapters = entry['chapters']
            # Transcripts come from seed_files/transcripts/*.txt; only files marked "STATUS: done" are shown
            status, text = read_transcript(entry.get('name') or chapter.name, slug)
            if status is not None:
                chapter.transcript = text if status == 'done' and text else None
                published += status == 'done'
            updated += 1
        db.session.commit()
        print(f'Updated {updated} chapters ({published} transcripts marked done and published).')
        if missing:
            print(f'No chapter found for slugs: {missing}')


if __name__ == '__main__':
    main()
