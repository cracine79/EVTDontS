from flask_restx import Namespace, Resource
from flask import request

retrieve_ns = Namespace('retrieve', description = 'A namespace for data retrieval')


@retrieve_ns.route('/password')
class RetrievePassword(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email')
        print(email)