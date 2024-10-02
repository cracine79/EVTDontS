from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User, QuestionTopic
from flask import request, jsonify

quiz_ns = Namespace('quiz', description="a namespace for getting quiz qusetions and answers")
from flask_jwt_extended import jwt_required, get_jwt_identity

@quiz_ns.route('/questions')
class AccessQuiz(Resource):
    @jwt_required()
    def get(self):
        type = request.args.get('type')
        chapter_id = request.args.get('chapter')
        topics = request.args.get('topics')
        topics_list = topics.split(',') if topics else []

        print("CHAPPPPTTTER", chapter_id)

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id

        topics = QuestionTopic.query.filter_by(chapter_id=chapter_id).all()
        questions = []
        
        if len(topics)>1:
            for topic in topics:
                topic_questions = Question.query.filter_by(topic_id=topic.id).limit(3).all()
                questions.extend(topic_questions)
        else:
            topic_questions = Question.query.filter_by(topic_id=topics[0].id).limit(6).all()
            questions.extend(topic_questions)
    
        question_ids = [question.id for question in questions]
        performances = UserPerformance.query.filter(UserPerformance.user_id == user_id, UserPerformance.question_id.in_(question_ids)).all()
        
        question_dict = {}
        for question in questions:

            answers = {
                answer.id: {  
                 'text': answer.text,
                'is_correct': answer.is_correct
                }
            for answer in question.answers
            }
            question_dict[question.id] = {
                "text": question.text,
                "topic_id": question.topic_id,
                'image_url': question.image_url,
                "answers": answers
            }
        
        for performance in performances:
            question_dict[performance.question_id]['correct'] = performance.is_correct
        # print (question_dict)
        return question_dict
