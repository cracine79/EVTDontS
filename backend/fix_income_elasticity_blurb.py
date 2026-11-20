"""One-off: fix the "…the next. us, you'll…" typo in the 3.5 Income Elasticity of Demand blurb
("Trust us, you'll…"). Safe to re-run.

    python fix_income_elasticity_blurb.py                     # locally, from backend/
    heroku run python backend/fix_income_elasticity_blurb.py  # production
"""
from config import ProdConfig
from exts import db
from main import create_app
from models import Chapter

app = create_app(ProdConfig)

OLD = 'bargain hunter the next. us, you'
NEW = 'bargain hunter the next. Trust us, you'

if __name__ == '__main__':
    with app.app_context():
        fixed = 0
        for ch in Chapter.query.filter(Chapter.video_blurb.contains(OLD)).all():
            ch.video_blurb = ch.video_blurb.replace(OLD, NEW)
            fixed += 1
        db.session.commit()
        print(f'Fixed {fixed} blurb(s).' if fixed else 'Nothing to fix (already corrected).')
