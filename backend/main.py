from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import User
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

#to protect a route(require signin), decorate the route with @jwt_required()

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)
JWTManager(app)

api = Api(app, doc='/docs')



signup_model = api.model(
    'Signup',
    { 
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model = api.model(
    'Login',
    { 
        "username":fields.String(),
        "password":fields.String()
    }
)


@api.route('/hello')
class HelloResource(Resource):
    @jwt_required()
    def get(self):
        return {"message":"Hello World"}

@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        data=request.get_json()

        username=data.get('username')

        db_user=User.query.filter_by(username=username).first()
        print(db_user)

        if db_user is not None:
            return jsonify({"message":f"User with username {username} already exists"})

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash= generate_password_hash(data.get('password'))           
        )

        new_user.save()

        return jsonify({"message":f"User {username} successfully signed up"})
    
    

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data=request.get_json()

        username = data.get('username')
        password = data.get('password')

        db_user = User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password_hash, password):
            #must pass in identity to include in access token
            access_token = create_access_token(db_user.username)
            refresh_token = create_refresh_token(db_user.username)

            return jsonify(
                {
                    "access_token":access_token,
                    "refresh_token":refresh_token
                }
            )



@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "User":User
    }


if __name__=="__main__":
    app.run()