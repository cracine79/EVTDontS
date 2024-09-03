from exts import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime

class Base(DeclarativeBase):
    pass

"""
    class: User
    id: integer
    email: string
    password: string
"""
user_unit_association = db.Table(
    'user_unit',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id'), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password_hash: Mapped[str]

    units: Mapped[list["Unit"]] = relationship(
        'Unit',
        secondary=user_unit_association,
        back_populates='users'
    )

    video_progress: Mapped["UserChapterProgress"] = relationship('UserChapterProgress', back_populates='user')


    def __repr__(self):
        return f"User <{self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()




class Unit(db.Model):
    __tablename__ = 'unit'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    chapters = relationship('Chapter', back_populates='unit')
    users: Mapped[list["User"]] = relationship(
        'User',
        secondary=user_unit_association,
        back_populates='units'
    )
    subject: Mapped[str] = mapped_column

    def __repr__(self):
        return f"Unit <{self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Chapter(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey('unit.id'))
    video_url: Mapped[str] = mapped_column(String(255))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    unit: Mapped["Unit"] = relationship('Unit', back_populates='chapters')
    questions: Mapped[list["Question"]] = relationship('Question', back_populates='chapter')

    def __repr__(self):
        return f"Chapter <{self.name}>"

class Question(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'))
    topic_id: Mapped[int] = mapped_column(ForeignKey('question_topic.id'))

    chapter: Mapped["Chapter"] = relationship('Chapter', back_populates='questions')
    topic: Mapped["QuestionTopic"] = relationship('QuestionTopic', back_populates='questions')
    answers: Mapped[list["Answer"]] = relationship('Answer', back_populates='question')

    def __repr__(self):
        return f"Question <{self.id}>"


class QuestionTopic(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    questions: Mapped[list["Question"]] = relationship('Question', back_populates='topic')

    def __repr__(self):
        return f"Topic <{self.name}>"


class Answer(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    question: Mapped["Question"] = relationship('Question', back_populates='answers')


class UserPerformance(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)

class UserChapterProgress(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'), nullable=False)
    video_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    quiz_grade: Mapped[int] = mapped_column(Integer, nullable=True)
    # completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship('User', back_populates='video_progress')
    chapter = relationship('Chapter')

    def __repr__(self):
        return f"Progress for user<{self.user_id}> on video in chapter{self.chapter_id}"