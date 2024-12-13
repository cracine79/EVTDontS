from flask_restx import Namespace, Resource, fields
from flask_wtf.csrf import generate_csrf
from flask import jsonify


csrf_ns = Namespace('csrf', description='A namespace for csrf')

@csrf_ns.route('/getit')
class getCsrf(Resource):
    def get(self):
        csrf_token = generate_csrf()
        return jsonify({
            'csrf_token':csrf_token
            })