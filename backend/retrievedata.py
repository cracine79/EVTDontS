from flask_restx import Namespace, Resource

retrieve_ns = Namespace('retrieve', description = 'A namespace for data retrieval')


@retrieve_ns.route('/password')
class RetrievePassword(Resource):
    def post(self):
        print('HELLO')