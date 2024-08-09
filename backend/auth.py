from flask_restx import Namespace, Resource, fields
from models import User
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_ns=Namespace('auth', description='A namespace for authentication')

signup_model = auth_ns.model(
    'Signup',
    { 
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model = auth_ns.model(
    'Login',
    { 
        "username":fields.String(),
        "password":fields.String()
    }
)
@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
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
    


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
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

    
    

