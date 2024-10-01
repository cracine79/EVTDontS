from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response, session
from exts import db
from models import UserChapterProgress, Chapter, User, UserPerformance
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

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
        answers = data.get('answers')

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id
        
        print("GRADDE", quiz_grade)
        print("CHAPTER", chapter_id)
        print("ANSWERS", answers)

        finished_chapter = Chapter.query.get(chapter_id)
        current_unit = finished_chapter.unit
        answer_response_data = {}

        for question_id, answer_data in answers.items():
     
            answer = UserPerformance(
                user_id = user_id, 
                question_id = question_id,
                is_correct=answer_data['isCorrect'], 
                answered_at=datetime.now() 
            )

            db.session.add(answer)
            db.session.flush()
            answer_response_data[answer.id]={
                'questionId': question_id, 
                'isCorrect': answer_data['isCorrect'], 
                'answerId': answer_data['answerId'],
                 'answeredAt': answer.answered_at }
        
        progress = UserChapterProgress.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()
        print("PROGRESS AND GRADESSS!!", progress, quiz_grade)

        if progress:
            progress.quiz_grade = quiz_grade
        else:
            progress = UserChapterProgress(user_id=user_id, chapter_id=chapter_id)
        
        db.session.commit()

        print("PROGRESS AND GRADESSS!!", progress, quiz_grade)

        # unit_chapters = Chapter.query.filter_by(unit_id=current_unit.id).order_by(Chapter.order).all()
        # print(unit_chapters)
        # done = False

        # if finished_chapter == unit_chapters[-1]:
        #     print('lastChapter!!')
        #     user_units = user.units
        #     current_unit_index = user_units.index(current_unit)
        #     print('currtentUnitIndex!!', current_unit_index)

        #     if current_unit_index +1 < len(user_units):
        #         next_unit = user_units[current_unit_index+1]
        #         print('NEXTUNITTTT!',next_unit)
        #         print('NEXTCHAPTER!!', next_unit.chapters[0])
        #         user.current_chapter = next_unit.chapters[0]
        #     else:
        #         user.current_chapter = None
        #         done = True
        # else:
        #     print('NOT LAST CHAPTER')
        #     next_chapter_index = unit_chapters.index(finished_chapter) + 1
        #     print(next_chapter_index)
        #     print(unit_chapters[next_chapter_index])
        #     user.current_chapter = unit_chapters[next_chapter_index]
        
        # db.session.commit()

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
            # "completed": done,
            "answers": answer_response_data
            }
                ))

@progress_ns.route('/chapter')
class ChapterProgress(Resource):
    @jwt_required()
    def patch(self):

        data=request.get_json()

        chapter_id = data.get('chapter_id')
        finished_chapter = Chapter.query.get(chapter_id)
        current_unit = finished_chapter.unit
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        unit_chapters = Chapter.query.filter_by(unit_id=current_unit.id).order_by(Chapter.order).all()

        done = False

        if finished_chapter == unit_chapters[-1]:
            print('lastChapter!!')
            user_units = user.units
            current_unit_index = user_units.index(current_unit)
            print('currtentUnitIndex!!', current_unit_index)

            if current_unit_index +1 < len(user_units):
                next_unit = user_units[current_unit_index+1]
                print('NEXTUNITTTT!',next_unit)
                print('NEXTCHAPTER!!', next_unit.chapters[0])
                user.current_chapter = next_unit.chapters[0]
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

        return (jsonify({
            'current_chapter':  user.current_chapter.id,
            'completed': done
        }))
   

        
