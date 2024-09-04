from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response, session
from exts import db
from models import UserChapterProgress, Chapter

progress_ns=Namespace('progress', description="a namespace for updating progress")


@progress_ns.route('/create')
class CreateChapterProgress(Resource):
    def post(self, user_id, chapter_id):
        progress = UserChapterProgress(user_id = user_id, chapter_id = chapter_id)
        db.session.add(progress)

        chapter = Chapter.get(chapter_id)

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