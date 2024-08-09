from flask import Flask
from flask_restx import Api
from models import User
from exts import db
from flask_jwt_extended import JWTManager
from auth import auth_ns

#to protect a route(require signin), decorate the route with @jwt_required()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    JWTManager(app)

    api = Api(app, doc='/docs')

    api.add_namespace(auth_ns)

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