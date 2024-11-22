from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_restx import Api
from backend.models import User
from backend.exts import db
from flask_jwt_extended import JWTManager
from backend.auth import auth_ns
from backend.questions import questions_ns
from backend.csrf import csrf_ns
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_migrate import Migrate
from backend.progress import progress_ns
from backend.quiz import quiz_ns
from backend.results import results_ns
from backend.units import units_ns
from backend.chapters import chapters_ns
from backend.topics import topics_ns
from backend.retrievedata import retrieve_ns
from dotenv import load_dotenv
import os

#to protect a route(require signin), decorate the route with @jwt_required()

def create_app(config):
    load_dotenv()
    app = Flask(__name__)

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    
    CORS(app)
    app.config.from_object(config)

    db.init_app(app)
    JWTManager(app)
    # csrf = CSRFProtect()
    # csrf.init_app(app)
    api = Api(app, doc='/docs')

    migrate = Migrate(app, db)

    api.add_namespace(auth_ns)
    api.add_namespace(questions_ns)
    api.add_namespace(csrf_ns)
    api.add_namespace(progress_ns)
    api.add_namespace(quiz_ns)
    api.add_namespace(results_ns)
    api.add_namespace(units_ns)
    api.add_namespace(chapters_ns)
    api.add_namespace(topics_ns)
    api.add_namespace(retrieve_ns)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "user":User
        }   

    return app


# @api.route('/hello') 
# class HelloResource(Resource):
#     @jwt_required()
#     def get(self):
#         return {"message":"Hello World"}







# if __name__=="__main__":
#     app.run()