from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response, session
from exts import db
from models import UserChapterProgress, Chapter, User
from flask_jwt_extended import get_jwt_identity, jwt_required

progress_ns=Namespace('progress', description="a namespace for updating progress")


@progress_ns.route('/')
class CreateChapterProgress(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        if not user:
            return jsonify({"message": "User not found"}), 404
        chapter_id = data.get('chapter_id')

        progress = UserChapterProgress(user_id = user_id, chapter_id = chapter_id)
        print(f"Progress is {progress} progID = {progress.user_id} chapId is {progress.chapter_id}")
        db.session.add(progress)

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        print(f"chapter is {chapter} MANNNNN")

        db.session.commit()

        return jsonify({
            chapter_id:{
                "name": chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url,
                "video_completed": progress.video_completed,
                "quiz_grade": progress.quiz_grade
            }
        })

    @jwt_required()
    def patch(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        if not user:
            return jsonify({"message": "User not found"}), 404
        chapter_id = data.get('chapter_id')

        progress = UserChapterProgress.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()
        print(f"progress is {progress} DUDDEORAMMMMMMA")
        if progress:
            progress.video_completed = True
        else:
            progress = UserChapterProgress(user_id = user_id, chapter_id=chapter_id, video_completed=True)
        print(f"completed is {progress.video_completed}")
        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        print(f"chapte name is {chapter.name}")
        print(f"chapter is {chapter}")
        print (f"chapter is {chapter} HOMMMMIE")
        print(f"name is {chapter.name}")
        print(chapter.unit_id)
        print(chapter.video_url)
        print(progress.video_completed)
        print(progress.quiz_grade)
        chapter_object =  {chapter_id:{
                "name": chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url,
                "video_completed": progress.video_completed,
                "quiz_grade": progress.quiz_grade
            }}
      
        return jsonify( chapter_object )
    
@progress_ns.route('/finishquiz')
class QuizProgress(Resource):
    @jwt_required()
    def put(self):
        
        data = request.get_json()
        quiz_grade = data.get('quiz_score')
        chapter_id = data.get('chapter_id')

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        finished_chapter = Chapter.query.get(chapter_id)
        current_unit = finished_chapter.unit
        
        progress = UserChapterProgress.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()
        print("PROGRESS AND GRADESSS!!", progress, quiz_grade)

        if progress:
            progress.quiz_grade = quiz_grade
        else:
            progress = UserChapterProgress(user_id=user_id, chapter_id=chapter_id)
        
        db.session.commit()
        
        print("PROGRESS AND GRADESSS!!", progress, quiz_grade)

        unit_chapters = Chapter.query.filter_by(unit_id=current_unit.id).order_by(Chapter.order).all()
        print(unit_chapters)
        done = False

        if finished_chapter == unit_chapters[-1]:
            print('lastChapter!!')
            user_units = user.units
            current_unit_index = user_units.index(current_unit)

            if current_unit_index +1 < len(user_units):
                next_unit = user_units[current_unit_index+1]
                user.current_chapter = next_unit.chapters[0].id
            else:
                user.current_chapter = None
                done = True
        else:
            print('NOT LAST CHAPTER')
            next_chapter_index = unit_chapters.index(finished_chapter) + 1
            print(next_chapter_index)
            print(unit_chapters[next_chapter_index])
            user.current_chapter = unit_chapters[next_chapter_index]
        
        db.session.commit()

        if user.current_chapter:
            current_chapter = user.current_chapter.id
        else:
            current_chapter = None

        chapter_dict = {
            finished_chapter.id: {
                "name": finished_chapter.name,
                'unit_id': finished_chapter.unit_id,
                'video_url': finished_chapter.video_url,
                'video_completed': True,
                'quiz_grade': quiz_grade
            }
        }
        return (jsonify({
            "user":{
                "username": user.username,
                "email": user.email,
                "current_chapter": current_chapter
                 },
            "chapters": chapter_dict,
            "completed": done
            }
                ))


        
