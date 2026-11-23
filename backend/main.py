from flask import Flask, Response, abort, redirect, render_template, request, url_for, send_from_directory, jsonify
from flask_restx import Api
from models import User
from exts import db
from flask_jwt_extended import JWTManager
from auth import auth_ns
from flask_cors import CORS
from flask_compress import Compress
from flask_migrate import Migrate
from progress import progress_ns
from quiz import quiz_ns
from results import results_ns
from units import units_ns
from chapters import chapters_ns
from topics import topics_ns
from retrievedata import retrieve_ns
from dotenv import load_dotenv
import os
from mail import mail_ns
from public import public_bp
from rate_limits import limiter
from werkzeug.middleware.proxy_fix import ProxyFix

#to protect a route(require signin), decorate the route with @jwt_required()
migrate = Migrate()

def create_app(config):
    load_dotenv()
    app = Flask(__name__)

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    
    CORS(app)
    app.config.from_object(config)
    Compress(app)  # gzip/brotli for HTML, CSS, JS and JSON
    limiter.init_app(app)

    db.init_app(app)
    JWTManager(app)
    api = Api(app, doc='/docs', prefix='/api')
    
    if app.config["ENV"] == "production":
        # Heroku's router sits in front of the app: trust its X-Forwarded-For/Proto so rate limits
        # see each visitor's real IP (not the router's) and URLs are built as https
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
        migrate_directory = 'backend/migrations'
    else:
        migrate_directory = 'migrations'
    
    migrate.init_app(app, db, directory=migrate_directory)

    api.add_namespace(auth_ns)
    api.add_namespace(progress_ns)
    api.add_namespace(quiz_ns)
    api.add_namespace(results_ns)
    api.add_namespace(units_ns)
    api.add_namespace(chapters_ns)
    api.add_namespace(topics_ns)
    api.add_namespace(retrieve_ns)
    api.add_namespace(mail_ns)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "user":User
        }   

    # Public SEO pages, sitemap/robots, the SPA at /app, and legacy redirects.
    # Registered last so the /api routes above take precedence.
    app.register_blueprint(public_bp)

    return app


# @api.route('/hello') 
# class HelloResource(Resource):
#     @jwt_required()
#     def get(self):
#         return {"message":"Hello World"}







# if __name__=="__main__":
#     app.run()