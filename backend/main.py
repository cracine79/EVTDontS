from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import User
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

api = Api(app, doc='/docs')



signup_model = api.model(
    'Signup',
    { 
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)


@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}

@api.route('/signup')
class Signup(Resource):
    # @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        # return {"message":"Hello World"}
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

        # return new_user, 201
        return jsonify({"message":f"User {username} successfully signed up"})
    
    

@api.route('/login')
class Login(Resource):
    def post(self):
        pass


@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "User":User
    }


if __name__=="__main__":
    app.run()