from flask_restx import Namespace, Resource, fields
from models import Chapter
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response
from sqlalchemy import text
from exts import db

chapters_ns = Namespace('chapters', description='A namespace for chapters')


@chapters_ns.route('/getall')
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
        # print('CHAPTER ID', chapter_id)
        chapter = Chapter.query.get_or_404(chapter_id)
        # print('GOT ID DUDE', chapter)
        return jsonify({
            'chapter_id': chapter.id,
            'video_blurb': chapter.video_blurb
        })
    
@chapters_ns.route('/search/<string:search_terms>')
class SearchChapters(Resource):
    def get(self, search_terms):
        or_query = ' | '.join(search_terms.split())
        print(or_query)

        chapters = db.session.query(
            Chapter,
            db.func.ts_rank(Chapter.search_vector, text("to_tsquery('english', :terms)")).label('rank')
        ).filter(
            Chapter.search_vector.op('@@')(text("to_tsquery('english', :terms)"))
        ).params(terms=or_query).order_by(db.desc('rank')).all()

        result = [{
            'id': chapter.id,
            'name': chapter.name,
            'quiz_blurb': chapter.quiz_blurb,
            'video_blurb': chapter.video_blurb,
            'video_url': chapter.video_url,
            'rank': rank
        } for chapter, rank in chapters
        ]

        return{'chapters': result}, 200

