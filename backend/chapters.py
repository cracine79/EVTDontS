from flask_restx import Namespace, Resource, fields
from models import Chapter
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response

chapters_ns = Namespace('chapters', description='A namespace for chapters')


@chapters_ns.route('/')
class GetChapters(Resource):
    def get(self):
        chapters = Chapter.query.all()
        print('CHAPPTERSSS MOFOO', chapters)t