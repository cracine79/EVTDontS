"""Topic mastery and review selection, computed from a student's answer history (UserPerformance).

How a topic's mastery score works:
  * Recent answers count more. The newest answer has weight 1, the one before it RECENCY_DECAY,
    then RECENCY_DECAY**2, and so on, so an old bad streak fades as the student improves.
  * Thin data is pulled toward 50% (a "prior" of half a right + half a wrong answer), so 1-for-1 isn't
    treated as mastered and 0-for-1 isn't treated as hopeless.
  * The score is compared to fixed thresholds (not the student's own average).

How the weak-spot quiz picks topics:
  * Topics below MASTERED, weakest first.
  * Plus mastered topics that are "due" again: each study session (day) in a row that the student
    passes pushes the next review further out (spaced repetition: 2, 4, 7, 14, 30, 60 days), so
    mastered material comes back before it's forgotten.

How questions are picked within a topic:
  * Questions they got wrong last time first, then questions they've never seen,
    then the ones they saw longest ago.
"""
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from exts import db
from models import Question, UserPerformance

# ---- tuning knobs ----
RECENCY_DECAY = 0.85           # weight of each older answer relative to the next newer one
PRIOR_RIGHT, PRIOR_WRONG = 0.5, 0.5   # like starting every topic with half a right and half a wrong answer
NEEDS_WORK = 0.70              # below this: "needs work"
MASTERED = 0.85                # at or above this (with enough evidence): "mastered"
MIN_EVIDENCE = 3.0             # weighted answers needed before a topic can count as mastered
REVIEW_INTERVALS_DAYS = [2, 4, 7, 14, 30, 60]   # next review after 1, 2, 3... passed sessions in a row
SESSION_PASS = 0.8             # a day's answers on a topic "pass" at 80% or better
WEAK_TOPIC_RECHECK_DAYS = 1


@dataclass
class TopicMastery:
    topic_id: int
    score: float               # 0..1, recency-weighted and smoothed
    evidence: float            # weighted number of answers behind the score
    attempts: int
    review_streak: int         # study sessions (days) in a row passed on this topic, newest first
    last_answered: datetime
    status: str                # 'learning' | 'needs_work' | 'getting_there' | 'mastered'
    due_at: datetime
    is_due: bool

    @property
    def percent(self):
        return round(self.score * 100)


def _history(user_id, topic_ids=None):
    """{topic_id: [(question_id, is_correct, answered_at), ...newest first]}"""
    q = (db.session.query(UserPerformance.question_id, UserPerformance.is_correct,
                          UserPerformance.answered_at, Question.topic_id)
         .join(Question, Question.id == UserPerformance.question_id)
         .filter(UserPerformance.user_id == user_id))
    if topic_ids is not None:
        q = q.filter(Question.topic_id.in_(list(topic_ids)))
    by_topic = defaultdict(list)
    for question_id, is_correct, answered_at, topic_id in q.all():
        by_topic[topic_id].append((question_id, bool(is_correct), answered_at))
    for answers in by_topic.values():
        answers.sort(key=lambda a: a[2], reverse=True)
    return by_topic


def _review_streak(answers):
    """Consecutive study days (newest first) where the student got at least SESSION_PASS right."""
    by_day = {}
    for _, is_correct, answered_at in answers:          # newest first
        right, total = by_day.get(answered_at.date(), (0, 0))
        by_day[answered_at.date()] = (right + is_correct, total + 1)
    streak = 0
    for day in sorted(by_day, reverse=True):
        right, total = by_day[day]
        if right / total < SESSION_PASS:
            break
        streak += 1
    return streak


def _score(answers, now):
    weight, weighted_right, evidence = 1.0, 0.0, 0.0
    for _, is_correct, _ in answers:                    # newest first
        evidence += weight
        weighted_right += weight * is_correct
        weight *= RECENCY_DECAY
    score = (weighted_right + PRIOR_RIGHT) / (evidence + PRIOR_RIGHT + PRIOR_WRONG)
    streak = _review_streak(answers)

    if evidence < MIN_EVIDENCE and score >= MASTERED:
        status = 'learning'
    elif score < NEEDS_WORK:
        status = 'needs_work'
    elif score < MASTERED or evidence < MIN_EVIDENCE:
        status = 'getting_there'
    else:
        status = 'mastered'

    last = answers[0][2]
    if status == 'mastered':
        interval = REVIEW_INTERVALS_DAYS[min(max(streak, 1), len(REVIEW_INTERVALS_DAYS)) - 1]
    else:
        interval = WEAK_TOPIC_RECHECK_DAYS
    due_at = last + timedelta(days=interval)
    return score, evidence, streak, status, due_at


def topic_mastery(user_id, topic_ids=None, now=None):
    """{topic_id: TopicMastery} for every topic the student has answered questions in."""
    now = now or datetime.now()
    out = {}
    for topic_id, answers in _history(user_id, topic_ids).items():
        score, evidence, streak, status, due_at = _score(answers, now)
        out[topic_id] = TopicMastery(topic_id, score, evidence, len(answers), streak, answers[0][2],
                                     status, due_at, now >= due_at)
    return out


def pick_review_topics(mastery, limit=4):
    """Weakest not-yet-mastered topics first, plus mastered topics that are due for a refresher."""
    not_mastered = sorted((m for m in mastery.values() if m.status != 'mastered'), key=lambda m: m.score)
    due_mastered = sorted((m for m in mastery.values() if m.status == 'mastered' and m.is_due),
                          key=lambda m: m.due_at)
    picks = [m.topic_id for m in not_mastered[:limit]]
    # Keep one slot for a spaced-repetition refresher when there's one due
    if due_mastered and len(picks) == limit:
        picks[-1] = due_mastered[0].topic_id
    for m in due_mastered:
        if len(picks) >= limit:
            break
        if m.topic_id not in picks:
            picks.append(m.topic_id)
    return picks


def pick_questions(topic_id, n, history_answers, exclude_ids=()):
    """Up to n questions from a topic: last-missed first, then unseen, then least recently seen."""
    exclude_ids = set(exclude_ids)
    pool = [q for q in Question.query.filter_by(topic_id=topic_id).all() if q.id not in exclude_ids]
    latest = {}
    for question_id, is_correct, answered_at in history_answers:   # newest first
        latest.setdefault(question_id, (is_correct, answered_at))

    missed = [q for q in pool if q.id in latest and not latest[q.id][0]]
    unseen = [q for q in pool if q.id not in latest]
    seen_right = sorted((q for q in pool if q.id in latest and latest[q.id][0]), key=lambda q: latest[q.id][1])
    random.shuffle(missed)
    random.shuffle(unseen)

    # Mix: up to half missed questions, then fresh ones, then anything else
    half = max(1, (n + 1) // 2)
    ordered = missed[:half] + unseen + missed[half:] + seen_right
    return ordered[:n]


def build_review_quiz(user_id, fallback_topic_ids=(), max_topics=4, max_questions=12):
    """Questions for the weak-spot quiz. Falls back to the given topics for students with no history."""
    mastery = topic_mastery(user_id)
    topic_ids = pick_review_topics(mastery, max_topics) if mastery else list(fallback_topic_ids)[:max_topics]
    if not topic_ids:
        return []
    history = _history(user_id, topic_ids)
    per_topic = max(3, max_questions // len(topic_ids))
    questions = []
    for topic_id in topic_ids:
        questions.extend(pick_questions(topic_id, per_topic, history.get(topic_id, []),
                                        exclude_ids={q.id for q in questions}))
    random.shuffle(questions)
    return questions[:max_questions]


def add_mastery(topic_progress_dict, user_id):
    """Add mastery_percent / mastery_status / review_due to a {topic_id: {...}} progress dict
    (what the API sends to the app), so screens can show mastery instead of all-time percent."""
    if not topic_progress_dict:
        return topic_progress_dict
    topic_ids = {int(k) for k in topic_progress_dict}
    mastery = topic_mastery(user_id, topic_ids)
    for key, entry in topic_progress_dict.items():
        m = mastery.get(int(key))
        entry['mastery_percent'] = m.percent if m else None
        entry['mastery_status'] = m.status if m else 'not_started'
        entry['review_due'] = bool(m and m.status == 'mastered' and m.is_due)
    return topic_progress_dict
