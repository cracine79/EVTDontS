from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, UserPerformance
from datetime import datetime
from backend.exts import db


results_ns=Namespace('results', description="A namespace for results")


@results_ns.route('/')
class AddResults(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        data = request.get_json()
        response_data = {}

        for question_id, answer_data in data.items():
     
            answer = UserPerformance(
                user_id = user_id, 
                question_id = question_id,
                is_correct=answer_data['isCorrect'], 
                answered_at=datetime.now() 
            )

            db.session.add(answer)
            db.session.flush()
            response_data[answer.id]={
                'questionId': question_id, 
                'isCorrect': answer_data['isCorrect'], 
                'answerId': answer_data['answerId'],
                 'answeredAt': answer.answered_at }
        db.session.commit()
        
        
        return (jsonify(response_data))
    
    

        