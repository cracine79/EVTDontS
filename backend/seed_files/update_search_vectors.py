from exts import db
from models import Chapter
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import text
from main import create_app
from config import ProdConfig

app=create_app(ProdConfig)

def update_search_vectors():
    chapters = Chapter.query.all()
    print(f"Found {len(chapters)} chapters to update.")
    for chapter in chapters:
        name = chapter.name or ''
        quiz_blurb = chapter.quiz_blurb or ''
        video_blurb = chapter.video_blurb or ''

        query = text("UPDATE chapter SET search_vector = to_tsvector('english', :content) WHERE id = :id")
        content = f"{name} {quiz_blurb} {video_blurb}"

        db.session.execute(query, {'content': content, 'id': chapter.id})
    db.session.commit()
    print("Search vectors updated.")

def main():
    with app.app_context():
        update_search_vectors()

if __name__ == "__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was a problem with the vector updates")

