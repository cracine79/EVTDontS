from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

questions_ns=Namespace('questions', description="A namespace for questions")


@questions_ns.route('/hello')
class HelloResource(Resource):
    @jwt_required()
    def get(self):
        return {"message":"Hello World"}