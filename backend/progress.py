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

        progress.video_completed = True
        db.session.commit()
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        return jsonify({
            chapter_id:{
                "name": chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url,
                "video_completed": progress.video_completed,
                "quiz_grade": progress.quiz_grade
            }
        })