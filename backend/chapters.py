from flask_restx import Namespace, Resource, fields
from backend.models import Chapter
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response

chapters_ns = Namespace('chapters', description='A namespace for chapters')


@chapters_ns.route('/')
class GetChapters(Resource):
    def get(self):
        chapters = Chapter.query.all()
        chapter_dict = {
            chapter.id: {
                'name': chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url
            } for chapter in chapters
        }

        return jsonify({
            'chapters': chapter_dict
        })

@chapters_ns.route('/blurb/<int:chapter_id>')
class GetChatperBlurb(Resource):
    def get(self, chapter_id):
        print('CHAPTER ID', chapter_id)
        chapter = Chapter.query.get_or_404(chapter_id)
        print('GOT ID DUDE', chapter)
        return jsonify({
            'chapter_id': chapter.id,
            'video_blurb': chapter.video_blurb
        })