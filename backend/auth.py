from flask_restx import Namespace, Resource, fields
from models import User, UserChapterProgress, UserTopicProgress, QuestionTopic
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

auth_ns=Namespace('auth', description='A namespace for authentication')

signup_model = auth_ns.model(
    'Signup',
    { 
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

@auth_ns.route('/refreshuser')
class RefreshUser(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if not user:
            return jsonify({"message": "User not found"}), 404
        
        user_units = user.units
        user_chapters = []
        for unit in user.units:
            chapters = unit.chapters
            user_chapters += chapters
        
        chapter_progress = UserChapterProgress.query.filter_by(user_id=user.id).all()
        
        progress_dict={
            chapter.chapter_id: {
                "video_completed": chapter.video_completed,
                "quiz_grade": chapter.quiz_grade
            } for chapter in chapter_progress
        }
        chapter_dict = {
            chapter.id: {
                "name": chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url
            } for chapter in user_chapters
        }
        
        units_dict = {unit.id: unit.name for unit in user_units}

        user_topic_progress = UserTopicProgress.query.filter_by(user_id=user.id).all()
        topic_progress_dict = {}

        for topic_progress in user_topic_progress:
            topic = QuestionTopic.query.get(topic_progress.topic_id)
            topic_name = topic.name
            if topic_progress.questions_asked > 0:
                percent_correct = int((topic_progress.answered_correctly/topic_progress.questions_asked)*100)
            else:
                percent_correct = 0

            topic_progress_dict[topic_progress.id] = {
                'topic_name': topic_name,
                'percent_correct': percent_correct,
                'chapter_id': topic.chapter_id,
                'topic_id': topic.id,
                'answered_correctly': topic_progress.answered_correctly,
                'questions_asked': topic_progress.questions_asked
            }

        chapter_progress = UserChapterProgress.query.filter_by(user_id=user.id).all()

        
        # for chapter_id, progress_data in progress_dict.items():
        #     if chapter_id in chapter_dict:
        #         chapter_dict[chapter_id].update(progress_data)
        #     else:
        #         chapter_dict[chapter_id] = progress_data            
        if user.current_chapter:
            current_chapter = user.current_chapter.id
        else:
            current_chapter=None

        if user:

            return jsonify({
               "user":{
                    "username": user.username,
                    "email": user.email,
                    "current_chapter": current_chapter
               },
               "units": units_dict,
               "chapters": chapter_dict,
               "topic_progress": topic_progress_dict,
               "user_chapters": progress_dict
               
                # Add any other user data you want to return
            })
        else:
            return jsonify({"message": "No user logged in"}), 200
        


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
        email = data.get('email')
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

        access_token = create_access_token(new_user.username)
        refresh_token = create_refresh_token(new_user.username)
        
        return jsonify({
            "user": {
                "access_token":access_token,
                "refresh_token":refresh_token,
                "email": email,
                "username": username
            },
            "message":f"User {username} successfully signed up",
            })
    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        print("starting")
        data = request.get_json()

        print("Request data:", data)  # Print the incoming request data

        username = data.get('username')
        password = data.get('password')

        print("Username:", username)
        print("Password:", password)

        db_user = User.query.filter_by(username=username).first()
        if db_user.current_chapter:
            current_chapter = db_user.current_chapter.id
            print(f"current_chapter is {current_chapter}")
        else:
            current_chapter=None
            print("no current chapter")

        if db_user:
            print("User found in database.")
            if check_password_hash(db_user.password_hash, password):
                print("Password matches.")
                access_token = create_access_token(db_user.username)
                refresh_token = create_refresh_token(db_user.username)

                user_units = db_user.units
                
                
                #extract all relevant chapters for user and send down on login
                
                user_chapters = []
                for unit in user_units:
                    chapters = unit.chapters
                    user_chapters += chapters

                chapter_progress = UserChapterProgress.query.filter_by(user_id=db_user.id).all()
                progress_dict={
                    chapter.chapter_id: {
                        "video_completed": chapter.video_completed,
                        "quiz_grade": chapter.quiz_grade
                    } for chapter in chapter_progress
                }
                print(f"progress_dict is {progress_dict}")
                chapter_dict = {
                    chapter.id: {
                        "name": chapter.name, 
                        "unit_id": chapter.unit_id,
                        "video_url": chapter.video_url,
                    } for chapter in user_chapters}
                units_dict = {unit.id: unit.name for unit in user_units}

                user_topic_progress = UserTopicProgress.query.filter_by(user_id=db_user.id).all()
                topic_progress_dict = {}

                for topic_progress in user_topic_progress:
                    topic = QuestionTopic.query.get(topic_progress.topic_id)
                    topic_name = topic.name
                    if topic_progress.questions_asked > 0:
                        percent_correct = int((topic_progress.answered_correctly/topic_progress.questions_asked)*100)
                    else:
                        percent_correct = 0

                    topic_progress_dict[topic_progress.id] = {
                        'topic_name': topic_name,
                        'percent_correct': percent_correct,
                        'chapter_id': topic.chapter_id,
                        'topic_id': topic.id,
                        'answered_correctly': topic_progress.answered_correctly,
                        'questions_asked': topic_progress.questions_asked
                    }
                user_chapter_dict = {}

                # for chapter_id, progress_data in progress_dict.items():
                #     if chapter_id in chapter_dict:
                #         chapter_dict[chapter_id].update(progress_data)
                #     else:
                #         chapter_dict[chapter_id] = progress_data            

                user_data = ({
                    "user": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "username": db_user.username,
                        "email": db_user.email,
                        "current_chapter": current_chapter
                        },
                    "units": units_dict,
                    "chapters": chapter_dict,
                    'topic_progress': topic_progress_dict,
                    "user_chapters": progress_dict
                
                })
                print(user_data)
                # print(jsonify(user_data))
                session['access_token'] = access_token
                return jsonify(user_data)
            else:
                print("Password does not match.")
        else:
            print("User not found.")

        return jsonify({"error": "problem logging in"})


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user=get_jwt_identity()
        new_access_token=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}),200)
