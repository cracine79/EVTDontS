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
        progress.video_completed = True
        print(f"completed is {progress.video_completed}")
        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        print(f"chapte name is {chapter.name}")
        print(f"chapter is {chapter}")
        # print (f"chapter is {chapter} HOMMMMIE")
        # print(f"name is {chapter.name}")
        # print(chapter.unit_id)
        # print(chapter.video_url)
        # print(progress.video_completed)
        # print(progress.quiz_grade)
        # chapter_object =  {chapter_id:{
        #         "name": chapter.name,
        #         'unit_id': chapter.unit_id,
        #         'video_url': chapter.video_url,
        #         "video_completed": progress.video_completed,
        #         "quiz_grade": progress.quiz_grade
        #     }}
      
        # return jsonify( chapter_object )