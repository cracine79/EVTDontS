from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_restx import Api
from models import User
from exts import db
from flask_jwt_extended import JWTManager
from auth import auth_ns
from questions import questions_ns
from csrf import csrf_ns
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_migrate import Migrate
from progress import progress_ns
from quiz import quiz_ns
from results import results_ns

#to protect a route(require signin), decorate the route with @jwt_required()

def create_app(config):
    app = Flask(__name__)
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