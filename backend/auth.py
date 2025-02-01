from flask_restx import Namespace, Resource, fields
from models import User, UserChapterProgress, UserTopicProgress, QuestionTopic, Chapter, UserPerformance
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from email_validator import validate_email, EmailNotValidError
from exts import db
from datetime import datetime

auth_ns=Namespace('auth', description='A namespace for authentication')

answers_model = auth_ns.model(
    'answers', {
        "questionId": fields.Integer(),
        "answerId": fields.Integer(),
        "isCorrect": fields.Boolean(),
        "topicId": fields.Integer(),
    }
)

quiz_data_model = auth_ns.model(
    'quizData', {
        "answers": fields.Nested(answers_model),
        "chapter_id": fields.Integer(),
        "quiz_score": fields.Integer(),

    }
)
signup_model = auth_ns.model(
    'Signup',
    { 
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String(),
        "quizData": fields.Nested(quiz_data_model, required=False),
    }
)

@auth_ns.route('/refreshuser')
class RefreshUser(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if not user:
            return jsonify({"message": "User not found"})
        
        user_units = user.units
        user_chapters = user.chapters
        
        
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
        units_dict = {}
        for unit in user_units:
            unit_chapters = [chapter for chapter in user_chapters if chapter.unit_id == unit.id]
            all_completed = all(
                (progress_dict.get(chapter.id, {}).get("quiz_grade") or 0) > 60
                for chapter in unit_chapters
            )
            units_dict[unit.id] = {
                "name": unit.name,
                "complete": all_completed
            }
        
        # units_dict = {unit.id: unit.name for unit in user_units}

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
            return ({"message": "No user logged in"}, 200)
        


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
        quizData = data.get('quizData', {})

       
        

        if db_user is not None:
            return ({"message":f"Someone is already using the username: {username}"}, 400)
        email = data.get('email')

        try:
            validate_email(email)
        except EmailNotValidError as e:
            return ({"message": f"Email is not valid: {str(e)}"}, 400)

        email_user = User.query.filter_by(email=email).first()
        if email_user is not None:
            return ({"message":f"Another user has already signed up with the email address {email}"}, 400)
        
        new_user = User(
            username=username,
            email=email,
            password_hash= generate_password_hash(data.get('password'))           
        )

        db.session.add(new_user)
        db.session.flush()
        new_user = User.query.filter_by(username=username).first()

        if quizData is not None:
            quizData = quizData.get('quizData', {})
            answers = quizData.get('answers', {})
            print("QUIZZ DATA", quizData)
            print('TRY THIS', answers)
 
            topic_response_data = {}

            for answer in answers.values():
                topicId = answer.get('topicId')
                if topicId in topic_response_data:
                    topic_response_data[topicId]['questions_asked'] += 1
                    if answer.get('isCorrect'):
                        topic_response_data[topicId]['answered_correctly']+=1
                else:
                                    topic_response_data[topicId] = {
                    'questions_asked': 1,
                    'answered_correctly': 1 if answer['isCorrect'] else 0
                }

                answer = UserPerformance(
                    user_id = new_user.id, 
                    question_id = answer.get('questionId'),
                    is_correct=answer.get('isCorrect'), 
                    answered_at=datetime.now() 
                )

                db.session.add(answer)
                db.session.flush()
            
            topic_progress_dict = {}
            topics_dict = {}
            
            for topic_id, response_data in topic_response_data.items():
                topic_progress = UserTopicProgress.query.filter_by(user_id=new_user.id, topic_id=topic_id).first()
                if topic_progress:
                    topic_progress.questions_asked += response_data['questions_asked']
                    topic_progress.answered_correctly += response_data['answered_correctly']
                else:
                    topic_progress = UserTopicProgress(
                        user_id=new_user.id, 
                        topic_id=topic_id, 
                        questions_asked = response_data['questions_asked'],
                        answered_correctly = response_data['answered_correctly'])
                    db.session.add(topic_progress)
                db.session.flush()
                

            percent_correct = int((topic_progress.answered_correctly/topic_progress.questions_asked)*100)
            topic = QuestionTopic.query.get(topic_progress.topic_id)


            topic_progress_dict[topic_id] = {
                'percent_correct': percent_correct,
                'questions_asked': topic_progress.questions_asked,
                'answered_correctly': topic_progress.answered_correctly,
                'topic_progress_id': topic_progress.id
            }

            topics_dict[topic_id] = {
                'chapter_id': topic.chapter_id,
                'topic_name': topic.name
            }     

            chapter_dict = {
                topic.chapter_id: {
                    'video_completed': True,
                    'quiz_grade': quizData['quiz_score']
                }
            }

            chapter = Chapter.query.filter_by(id=quizData.get('chapter_id')).first()
            print('NEW_USERRRRR', new_user)
            print('CHAPPPTER', chapter)
            progress = UserChapterProgress(user_id = new_user.id, chapter_id = chapter.id)
            db.session.add(progress)



        new_user.save()

        access_token = create_access_token(new_user.username)
        refresh_token = create_refresh_token(new_user.username)
        
        if quizData is None:
            return ({
                "user": {
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "email": email,
                    "username": username
                }}, 200)
        else:
            return ({
                "user": {
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "email": email,
                    "username": username
                },
                'topic_progress': topic_progress_dict, 
                'topics': topics_dict,
                'chapters': chapter_dict

                }, 200)
    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        # print("starting")
        data = request.get_json()

        # print("Request data:", data)  # Print the incoming request data

        username = data.get('username')
        password = data.get('password')

        # print("Username:", username)
        # print("Password:", password)

        db_user = User.query.filter_by(username=username).first()
        
        if db_user is None:
            return({"error": "Username not found"}, 404)
        
        if not check_password_hash(db_user.password_hash, password):
            return({"error": "Password does not match username"}, 401)


        if db_user:
            if check_password_hash(db_user.password_hash, password):
                access_token = create_access_token(db_user.username)
                refresh_token = create_refresh_token(db_user.username)

                user_units = db_user.units
                user_chapters = db_user.chapters

                if db_user.current_chapter:
                    current_chapter = db_user.current_chapter.id
                else:
                    current_chapter=None

                
                
                #extract all relevant chapters for user and send down on login
                
                # user_chapters = []
                # for unit in user_units:
                #     chapters = unit.chapters
                #     user_chapters += chapters

                chapter_progress = UserChapterProgress.query.filter_by(user_id=db_user.id).all()
                progress_dict={
                    chapter.chapter_id: {
                        "video_completed": chapter.video_completed,
                        "quiz_grade": chapter.quiz_grade
                    } for chapter in chapter_progress
                }
                chapter_dict = {
                    chapter.id: {
                        "name": chapter.name, 
                        "unit_id": chapter.unit_id,
                        "video_url": chapter.video_url,
                    } for chapter in db_user.chapters}
                # units_dict = {unit.id: unit.name for unit in user_units}
                units_dict = {}
                for unit in user_units:
                    unit_chapters = [chapter for chapter in user_chapters if chapter.unit_id == unit.id]
                    quiz_grades = []
                 
                    for chapter in unit_chapters:
                        the_quiz_grade = progress_dict[chapter.id].get("quiz_grade", 0)
                        if the_quiz_grade is not None:
                            quiz_grades.append(the_quiz_grade)
                        else:
                            quiz_grades.append(0) 
                    all_completed = all(grade > 60 for grade in quiz_grades)
                    units_dict[unit.id] = {
                        "name": unit.name,
                        "complete": all_completed
                    }

                user_topic_progress = UserTopicProgress.query.filter_by(user_id=db_user.id).all()
                topic_progress_dict = {}
                topic_dict = {}
                for topic_progress in user_topic_progress:
                    topic = QuestionTopic.query.get(topic_progress.topic_id)
                    topic_name = topic.name
                    if topic_progress.questions_asked > 0:
                        percent_correct = int((topic_progress.answered_correctly/topic_progress.questions_asked)*100)
                    else:
                        percent_correct = 0

                    topic_progress_dict[topic.id] = {
                        'percent_correct': percent_correct,
                        'topic_progress_id': topic_progress.id,
                        'answered_correctly': topic_progress.answered_correctly,
                        'questions_asked': topic_progress.questions_asked
                    }

                    topic_dict[topic.id] = {
                        'topic_name': topic_name,
                        'chapter_id': topic.chapter_id,
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
                    "user_chapters": progress_dict,
                    'topics': topic_dict
                
                })

                # print(jsonify(user_data))
                session['access_token'] = access_token
                code = 200
                return (user_data, 200)
            else:
                return jsonify({"error": "Password and username do not match"})
        else:
            return jsonify({"error": "Username not found"})

        return jsonify({"error": "problem logging in"})


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):

        current_user=get_jwt_identity()
        new_access_token=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}),200)



@auth_ns.route('/resetpassword')
class ResetPassword(Resource):
    def post(self):
        email = request.json.get('email')



