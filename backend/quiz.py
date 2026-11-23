from flask_restx import Namespace, Resource
from models import Question, Answer, UserPerformance, User, QuestionTopic, UserTopicProgress, Chapter, Unit, UserChapterProgress
from flask import request, jsonify
from urllib.parse import unquote
import json, random

from exts import db
from mastery import build_review_quiz, pick_questions, _history


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

# Chapter quiz length (also used for the free quiz), spread evenly across the chapter's topics.
CHAPTER_QUIZ_LENGTH = 8
# Unit quiz length, split evenly across the finished chapters and then across each chapter's topics.
# Capped by the questions available (small units get fewer until their question bank grows).
UNIT_QUIZ_LENGTH = 20
# Topic review quiz: this many per topic, or SINGLE_TOPIC_REVIEW when only one topic is chosen.
TOPIC_REVIEW_PER_TOPIC = 3
SINGLE_TOPIC_REVIEW = 6


def chapter_quiz_size(topic_question_counts):
    """How many questions a chapter quiz will have, given each topic's question count."""
    return min(CHAPTER_QUIZ_LENGTH, sum(topic_question_counts))


def split_across_topics(n, counts):
    """{topic_id: how many questions to take} so n questions are spread as evenly as possible.
    counts is {topic_id: questions available}. When n doesn't divide evenly, which topics get the
    extra question is random, so it rotates between attempts. A topic without enough questions
    passes its leftover share to the others."""
    take = {t: 0 for t in counts}
    order = list(counts)
    random.shuffle(order)
    remaining = min(n, sum(counts.values()))
    while remaining:
        for t in order:
            if remaining and take[t] < counts[t]:
                take[t] += 1
                remaining -= 1
    return take


def questions_across_topics(topic_ids, n, user_id=None):
    """n questions spread evenly over the given topics, grouped by topic in the order given.
    Within a topic: for a logged-in student, questions they last missed and ones they haven't seen
    come first (see mastery.pick_questions); otherwise a random pick."""
    topic_ids = list(dict.fromkeys(topic_ids))
    if not topic_ids:
        return []
    counts = dict(db.session.query(Question.topic_id, db.func.count(Question.id))
                  .filter(Question.topic_id.in_(topic_ids)).group_by(Question.topic_id).all())
    take = split_across_topics(n, {t: counts.get(t, 0) for t in topic_ids})
    history = _history(user_id, topic_ids) if user_id else {}
    questions = []
    for t in topic_ids:
        if take[t]:
            questions.extend(pick_questions(t, take[t], history.get(t, [])))
    return questions
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
            questions = questions_across_topics([t.id for t in sorted(topics, key=lambda t: t.id)],
                                                CHAPTER_QUIZ_LENGTH, user_id)

        elif type == 'topicQuiz':
            params_topics = request.args.get('topics')
            decoded_params_topics = unquote(params_topics)
            user_topics = json.loads(decoded_params_topics)
            topic_ids = [topic['topic_id'] for topic in user_topics]
            
            per_topic = TOPIC_REVIEW_PER_TOPIC if len(topic_ids) > 1 else SINGLE_TOPIC_REVIEW
            history = _history(user_id, topic_ids)
            for topic_id in topic_ids:
                # Last-missed and unseen questions first, so reviews don't repeat what they just saw
                questions.extend(pick_questions(topic_id, per_topic, history.get(topic_id, []),
                                                exclude_ids={q.id for q in questions}))
        
        elif type == 'unitQuiz':
            current_chapter_id = request.args.get('chapter')
            current_chapter = Chapter.query.get(current_chapter_id)
            current_unit = Unit.query.get(current_chapter.unit_id)
            completed_chapters = UserChapterProgress.query.filter_by(user_id=user_id).filter(UserChapterProgress.quiz_grade.isnot(None)).all()
            completed_chapter_ids = {progress.chapter_id for progress in completed_chapters}
            unit_chapters = sorted((c for c in current_unit.chapters if c.id in completed_chapter_ids),
                                   key=lambda c: c.order)
            # UNIT_QUIZ_LENGTH spread evenly over the finished chapters, then over each chapter's topics
            chapter_counts = {c.id: Question.query.filter_by(chapter_id=c.id).count() for c in unit_chapters}
            take = split_across_topics(UNIT_QUIZ_LENGTH, chapter_counts)
            for chapter in unit_chapters:
                if take[chapter.id]:
                    questions.extend(questions_across_topics(
                        [t.id for t in sorted(chapter.topics, key=lambda t: t.id)], take[chapter.id], user_id))

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
        questions = questions_across_topics([t.id for t in sorted(topics, key=lambda t: t.id)],
                                            CHAPTER_QUIZ_LENGTH)


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