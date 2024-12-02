from flask_restx import Namespace, Resource
from models import QuestionTopic
from flask import request, jsonify

topics_ns = Namespace('topics', description='A namespace for topics')

@topics_ns.route('/')
class GetTopics(Resource):
    def get(self):
        topics = QuestionTopic.query.all()
        topic_dict = {
            topic.id: {
                'topic_name': topic.name,
                'chapter_id': topic.chapter_id 
            } for topic in topics
        } 

        return jsonify({'topics':topic_dict})