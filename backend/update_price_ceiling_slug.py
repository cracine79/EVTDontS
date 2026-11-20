"""One-off: rename the 4.3 Price Ceilings slug from "price ceilings" (with a space)
to "price-ceilings" so its URL is /videos/price-ceilings. The old URL redirects."""
from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter

app = create_app(ProdConfig)

OLD, NEW = "price ceilings", "price-ceilings"


def main():
    with app.app_context():
        chapter = Chapter.query.filter_by(slug=OLD).first()
        if not chapter:
            print(f'No chapter with slug "{OLD}" (already updated?). Nothing to do.')
            return
        chapter.slug = NEW
        db.session.commit()
        print(f'Updated "{chapter.name}" slug: "{OLD}" -> "{NEW}"')


if __name__ == "__main__":
    main()
