from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User
from flask import request, jsonify

quiz_ns = Namespace('quiz', description="a namespace for getting quiz qusetions and answers")
from flask_jwt_extended import jwt_required, get_jwt_identity

@quiz_ns.route('/quiz')
class AccessQuiz(Resource):
    @jwt_required()
    def get(self):
        data = request.get_json()
        chapter_id = data.get('chapter_id')
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        questions = Question.query.filter_by(chapter_id=chapter_id).all()
        question_ids = [question.id for question in questions]
        performances = UserPerformance.query.filter(UserPerformance.user_id == user_id, UserPerformance.question_id.in_(question_ids)).all()
        
        question_dict = {}
        for question in questions:
            question_dict[question.id] = {
                "text": question.text,
                "topic_id": question.topic_id,
                "answers": question.answers
            }
        
        for performance in performances:
            question_dict[performance.question_id]['correct'] = performance.is_correct

        return question_dict
