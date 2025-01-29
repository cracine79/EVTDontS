from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User, QuestionTopic, UserTopicProgress, Chapter, Unit, UserChapterProgress
from flask import request, jsonify
from urllib.parse import unquote
from collections import defaultdict
import json, random, math

quiz_ns = Namespace('quiz', description="a namespace for getting quiz qusetions and answers")
from flask_jwt_extended import jwt_required, get_jwt_identity

@quiz_ns.route('/questions')
class AccessQuiz(Resource):
    @jwt_required()
    def get(self):
        type = request.args.get('type')
        chapter_id = request.args.get('chapter')
        
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id
        questions = []

        if type == 'chapterQuiz':
            topics = QuestionTopic.query.filter_by(chapter_id=chapter_id).all()
            chapter = Chapter.query.get(chapter_id)
            quiz_blurb = chapter.quiz_blurb
            quiz_blurb_img_url = chapter.quiz_blurb_img_url

            if len(topics)>1:
                for topic in topics:
                    topic_questions = Question.query.filter_by(topic_id=topic.id).limit(3).all()
                    questions.extend(topic_questions)
            else:
                topic_questions = Question.query.filter_by(topic_id=topics[0].id).limit(6).all()
                questions.extend(topic_questions)

        
        elif type == 'topicQuiz':
            params_topics = request.args.get('topics')
            decoded_params_topics = unquote(params_topics)
            user_topics = json.loads(decoded_params_topics)
            topic_ids = [topic['topic_id'] for topic in user_topics]
            
            if len(topic_ids)>1:
                for topic_id in topic_ids:
                    all_topic_questions = Question.query.filter_by(topic_id = topic_id).offset(3).all()
                    topic_questions = random.sample(all_topic_questions, min(3, len(all_topic_questions)))
                    questions.extend(topic_questions)
            else:
                all_topic_questions = Question.query.filter_by(topic_id = topic_ids[0]).offset(3).all()
                topic_questions = random.sample(all_topic_questions, min(6, len(all_topic_questions)))
                questions.extend(topic_questions)
        
        elif type == 'unitQuiz':
            current_chapter_id = request.args.get('chapter')
            current_chapter = Chapter.query.get(current_chapter_id)
            current_unit = Unit.query.get(current_chapter.unit_id)
            qnum =int(15/len(current_unit.chapters))
            unit_chapters = current_unit.chapters
            completed_chapters = UserChapterProgress.query.filter_by(user_id=user_id).filter(UserChapterProgress.quiz_grade.isnot(None)).all()
            completed_chapter_ids = {progress.chapter_id for progress in completed_chapters}
            completed_unit_chapters = {chapter for chapter in unit_chapters if chapter.id in completed_chapter_ids}
            for chapter in completed_unit_chapters:
                for topic in chapter.topics:
                    topic_questions = list(Question.query.filter_by(topic_id = topic.id).all())
                    questions_to_add = random.sample(topic_questions, min(qnum, len(topic_questions)))
                    questions.extend(questions_to_add)

        elif type in['shortWeakspotQuiz','longWeakspotQuiz']:
            progressArray = user.topic_progresses
            percentageList = {}
            numberTopics = 0
            percentSum = 0
            for progress in progressArray:
                percentCorrect = math.floor((progress.answered_correctly/progress.questions_asked)*100)
                percentageList[progress.topic_id] = (percentCorrect)
                numberTopics += 1
                percentSum += percentCorrect
            averageScore = percentSum/numberTopics
            topic_ids = []
            baselineScore = 50

            while len(topic_ids) < 3 and baselineScore <101:
                for key, value in percentageList.items():            
                    if value <= baselineScore and key not in topic_ids:
                        topic_ids.append(key)
                baselineScore += 10
            
            performances = UserPerformance.query.filter_by(user_id=user_id).all()
            for topic_id in topic_ids:
                all_topic_questions = Question.query.filter_by(topic_id = topic_id).all()

                question_ids = {question.id for question in all_topic_questions}
                question_performances = [performance for performance in performances if performance.question_id in question_ids]

                if(len(question_performances) > 0):
                    incorrect_counts = defaultdict(int)
                    total_counts = defaultdict(int)
                    
                    for performance in question_performances:
                        total_counts[performance.question_id] += 1
                        if not performance.is_correct:
                            incorrect_counts[performance.question_id] += 1

                    question_ids_with_high_failure_rate = {
                        question_id
                        for question_id in total_counts
                        if incorrect_counts[question_id] / total_counts[question_id] >= 0.5
                    }
                    questions_to_go = random.sample(question_ids_with_high_failure_rate, min(2, len(question_ids_with_high_failure_rate)))

                    for questionId in questions_to_go:
                        question_to_add = next((obj for obj in all_topic_questions if obj.id == questionId), None)
                        questions.append(question_to_add)

                asked_question_ids = {performance.question_id for performance in question_performances}    
                # print('QUESTIONS THAT ARE ANSWERED WRONG INCLUDE', questions)

                available_questions = [q for q in all_topic_questions if q not in questions and q.id not in asked_question_ids]
                target_count = 4 - len(questions_to_go)
                while len(available_questions) < target_count:
                    question = random.choice(all_topic_questions)
                    if question not in available_questions:
                        available_questions.append(question)


                while target_count > 0:
               
                    index_number = random.randint(0, len(available_questions) - 1)
                    selected_question = available_questions[index_number]

                    questions.append(selected_question)
                    target_count -=1

                    available_questions.pop(index_number)
                
                
            random.shuffle(questions)
            questions = questions[:12]


        question_ids = [question.id for question in questions]
        # performances = UserPerformance.query.filter(UserPerformance.user_id == user_id, UserPerformance.question_id.in_(question_ids)).all()
        
        question_dict = {}
        for question in questions:

            answers = {
                answer.id: {  
                 'text': answer.text,
                'is_correct': answer.is_correct
                }
            for answer in question.answers
            }
            question_dict[question.id] = {
                "text": question.text,
                "topic_id": question.topic_id,
                'image_url': question.image_url,
                "answers": answers
            }
        quiz_blurb = quiz_blurb if 'quiz_blurb' in locals() else None
        quiz_blurb_img_url = quiz_blurb_img_url if 'quiz_blurb_img_url' in locals() else None
        # for performance in performances:
        #     question_dict[performance.question_id]['correct'] = performance.is_correct
        return ({
            "questions": question_dict,
            "quiz_blurb": quiz_blurb,
            "quiz_blurb_img_url": quiz_blurb_img_url
        })
    
@quiz_ns.route('/questions_nouser')
class AccessQuizLoggedout(Resource):
    def get(self):
        
        chapter_id = request.args.get('chapter')
        print('CHAPTER ID', chapter_id)
        topics = QuestionTopic.query.filter_by(chapter_id=chapter_id).all()
        chapter = Chapter.query.get(chapter_id)
        quiz_blurb = chapter.quiz_blurb
        quiz_blurb_img_url = chapter.quiz_blurb_img_url
        questions = []

        if len(topics)>1:
            for topic in topics:
                topic_questions = Question.query.filter_by(topic_id=topic.id).limit(3).all()
                questions.extend(topic_questions)

        else:
            topic_questions = Question.query.filter_by(topic_id=topics[0].id).limit(6).all()
            questions.extend(topic_questions)
    

        question_ids = [question.id for question in questions]
        question_dict = {}

        for question in questions:

            answers = {
                answer.id: {  
                 'text': answer.text,
                'is_correct': answer.is_correct
                }
            for answer in question.answers
            }
            question_dict[question.id] = {
                "text": question.text,
                "topic_id": question.topic_id,
                'image_url': question.image_url,
                "answers": answers
            }
        quiz_blurb = quiz_blurb if 'quiz_blurb' in locals() else None
        quiz_blurb_img_url = quiz_blurb_img_url if 'quiz_blurb_img_url' in locals() else None

        
        return ({
            "questions": question_dict,
            "quiz_blurb": quiz_blurb,
            "quiz_blurb_img_url": quiz_blurb_img_url
        })