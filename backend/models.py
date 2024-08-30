from exts import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, text

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

    def __repr__(self):
        return f"Unit <{self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    video_url = db.Column(db.String(255))
    completed = db.Column(db.Boolean, default=False)
    unit = relationship('Unit', back_populates='chapters')
    questions = relationship('Question', back_populates='chapter')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('question_topic.id'))
    chapter = relationship('Chapter', back_populates='questions')
    topic = relationship('QuestionTopic', back_populates='questions')
    answers = relationship('Answer', back_populates='question')

class QuestionTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    questions = relationship('Question', back_populates='topic')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    is_correct = db.Column(db.Boolean, nullable=False)
    question = relationship('Question', back_populates='answers')

class UserPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False)