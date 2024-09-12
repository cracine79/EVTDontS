from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, UserPerformance
from datetime import datetime
from exts import db


results_ns=Namespace('results', description="A namespace for results")


@results_ns.route('/')
class AddResults(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        data = request.get_json()

        for question_id, answer_data in data.items():
            print(answer_data)
            answer = UserPerformance(
                user_id = user_id, 
                question_id = question_id,
                is_correct=answer_data['isCorrect'], 
                answered_at=datetime.now() 
            )

            db.session.add(answer)
        db.session.commit()

        