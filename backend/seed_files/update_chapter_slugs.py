from exts import db
from models import Chapter
from slugify import slugify
from run import create_app
from config import DevConfig

app = create_app(DevConfig)


def generate_slugs_for_existing_chapters():
    with app.app_context():
        chapters = Chapter.query.all()
        for chapter in chapters:
            # Generate a slug from the chapter title
            reduced_name = " ".join(chapter.name.split(" ")[1:])
            chapter.slug =slugify(reduced_name)
        db.session.commit()
        print(f"Slugs updated for {len(chapters)} chapters.")


if __name__ == '__main__':
    generate_slugs_for_existing_chapters()
