from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User


results_ns=Namespace('results', description="A namespace for results")


@results_ns.route('/')
class AddResults(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        data = request.get_json()
        # print(data.items())
        for question_id, answer in data.items():
            print(f"question id is{question_id}")