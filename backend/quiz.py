from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User, QuestionTopic, UserTopicProgress, Chapter, Unit, UserChapterProgress
from flask import request, jsonify
from urllib.parse import unquote
import json, random

from mastery import build_review_quiz

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
                    topic_questions = Question.query.filter_by(topic_id=topic.id).order_by(Question.id).limit(3).all()
                    questions.extend(topic_questions)
            else:
                topic_questions = Question.query.filter_by(topic_id=topics[0].id).order_by(Question.id).limit(6).all()
                questions.extend(topic_questions)

        
        elif type == 'topicQuiz':
            params_topics = request.args.get('topics')
            decoded_params_topics = unquote(params_topics)
            user_topics = json.loads(decoded_params_topics)
            topic_ids = [topic['topic_id'] for topic in user_topics]
            
            per_topic = 3 if len(topic_ids) > 1 else 6
            for topic_id in topic_ids:
                # Skip the questions reserved for the chapter quiz, unless that leaves nothing
                all_topic_questions = (Question.query.filter_by(topic_id=topic_id).order_by(Question.id).offset(3).all()
                                       or Question.query.filter_by(topic_id=topic_id).all())
                questions.extend(random.sample(all_topic_questions, min(per_topic, len(all_topic_questions))))
        
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

        elif type in ['shortWeakspotQuiz', 'longWeakspotQuiz']:
            # Mastery-based review: weakest topics first, plus mastered topics due for a refresher.
            # See mastery.py for how scores, statuses and review timing work.
            started = UserChapterProgress.query.filter_by(user_id=user_id).filter(
                (UserChapterProgress.video_completed.is_(True)) | (UserChapterProgress.quiz_grade.isnot(None))).all()
            fallback_chapter_ids = [p.chapter_id for p in started] or [c.id for c in user.chapters]
            fallback_topic_ids = [t.id for t in QuestionTopic.query.filter(
                QuestionTopic.chapter_id.in_(fallback_chapter_ids)).order_by(QuestionTopic.id).all()]
            questions = build_review_quiz(user_id, fallback_topic_ids,
                                          max_questions=20 if type == 'longWeakspotQuiz' else 12)

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
                topic_questions = Question.query.filter_by(topic_id=topic.id).order_by(Question.id).limit(3).all()
                questions.extend(topic_questions)

        else:
            topic_questions = Question.query.filter_by(topic_id=topics[0].id).order_by(Question.id).limit(6).all()
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