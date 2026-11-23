from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User, QuestionTopic, UserTopicProgress, Chapter, Unit, UserChapterProgress
from flask import request, jsonify
from urllib.parse import unquote
import json, random

from mastery import build_review_quiz


def rewatch_info(question):
    """The part of the video that explains this question, for the results page's "Rewatch this part" link.
    None when the question has no timestamp (or the chapter has no video)."""
    if question.video_start is None:
        return None
    from public import youtube_id  # here, not at the top: public imports this module
    ch = question.chapter
    yt = youtube_id(ch.video_url) if ch else None
    if not yt:
        return None
    # Name the key moment the timestamp falls in, e.g. "Proportion of Consumer Budget/Income"
    moments = sorted((m for m in (ch.video_chapters or []) if 'start' in m and m.get('label')), key=lambda m: m['start'])
    label = None
    for m in moments:
        if m['start'] <= question.video_start:
            label = m['label']
    return {'yt': yt, 'start': question.video_start, 'label': label, 'slug': ch.slug, 'chapter': ch.name}

quiz_ns = Namespace('quiz', description="a namespace for getting quiz qusetions and answers")

# Chapter quiz size (also used for the free quiz): this many questions from each topic,
# or SINGLE_TOPIC_QUESTIONS when the chapter has only one topic.
QUESTIONS_PER_TOPIC = 3
SINGLE_TOPIC_QUESTIONS = 6


def chapter_quiz_size(topic_question_counts):
    """How many questions a chapter quiz will have, given each topic's question count."""
    counts = list(topic_question_counts)
    if len(counts) == 1:
        return min(SINGLE_TOPIC_QUESTIONS, counts[0])
    return sum(min(QUESTIONS_PER_TOPIC, c) for c in counts)
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
                    topic_questions = Question.query.filter_by(topic_id=topic.id).order_by(Question.id).limit(QUESTIONS_PER_TOPIC).all()
                    questions.extend(topic_questions)
            else:
                topic_questions = Question.query.filter_by(topic_id=topics[0].id).order_by(Question.id).limit(SINGLE_TOPIC_QUESTIONS).all()
                questions.extend(topic_questions)

        
        elif type == 'topicQuiz':
            params_topics = request.args.get('topics')
            decoded_params_topics = unquote(params_topics)
            user_topics = json.loads(decoded_params_topics)
            topic_ids = [topic['topic_id'] for topic in user_topics]
            
            per_topic = 3 if len(topic_ids) > 1 else 6
            for topic_id in topic_ids:
                # Skip the questions reserved for the chapter quiz, unless that leaves nothing
                all_topic_questions = (Question.query.filter_by(topic_id=topic_id).order_by(Question.id).offset(QUESTIONS_PER_TOPIC).all()
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
                'rewatch': rewatch_info(question),
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
        chapter = Chapter.query.get(chapter_id) if chapter_id and str(chapter_id).isdigit() else None
        if chapter is None:
            return {'message': 'Chapter not found'}, 404
        topics = QuestionTopic.query.filter_by(chapter_id=chapter.id).all()
        quiz_blurb = chapter.quiz_blurb
        quiz_blurb_img_url = chapter.quiz_blurb_img_url
        questions = []

        if len(topics)>1:
            for topic in topics:
                topic_questions = Question.query.filter_by(topic_id=topic.id).order_by(Question.id).limit(QUESTIONS_PER_TOPIC).all()
                questions.extend(topic_questions)

        else:
            topic_questions = Question.query.filter_by(topic_id=topics[0].id).order_by(Question.id).limit(SINGLE_TOPIC_QUESTIONS).all()
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
                'rewatch': rewatch_info(question),
                "answers": answers
            }
        quiz_blurb = quiz_blurb if 'quiz_blurb' in locals() else None
        quiz_blurb_img_url = quiz_blurb_img_url if 'quiz_blurb_img_url' in locals() else None

        
        return ({
            "questions": question_dict,
            "quiz_blurb": quiz_blurb,
            "quiz_blurb_img_url": quiz_blurb_img_url
        })