from exts import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime
from typing import Optional

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
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name='user_unit_id'), primary_key=True),
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id', name='unit_user_id'), primary_key=True)
)

user_chapter_association = db.Table(
    'user_chapter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name='user_chapter_id'), primary_key=True),
    db.Column('chapter_id', db.Integer, db.ForeignKey('chapter.id', name='chapter_user_id'), primary_key=True)
)

class User(db.Model):
    __tablename__='user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str]=mapped_column(String(255), unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    units: Mapped[list["Unit"]] = relationship(
        'Unit',
        secondary=user_unit_association,
        back_populates='users'
    )

    chapters: Mapped[list["Chapter"]] = relationship(
        'Chapter',
        secondary=user_chapter_association,
        back_populates='users'
    )

    current_chapter_id: Mapped[Optional[int]] = mapped_column(ForeignKey('chapter.id'), nullable=True)
    current_chapter: Mapped['Chapter'] = relationship('Chapter', foreign_keys=[current_chapter_id])


    chapter_progress: Mapped[list["UserChapterProgress"]] = relationship(
        'UserChapterProgress', 
        back_populates='user')
    
    topic_progresses: Mapped[list['UserTopicProgress']] = relationship(
        'UserTopicProgress',
        back_populates='user'
    )

    performances: Mapped[list['UserPerformance']] = relationship(
        'UserPerformance', back_populates='user'
    )


    def __repr__(self):
        return f"User <{self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()




class Unit(db.Model):
    __tablename__ = 'unit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    chapters = relationship('Chapter', back_populates='unit')
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'), nullable=False)  # Foreign key for Subject

    users: Mapped[list["User"]] = relationship(
        'User',
        secondary=user_unit_association,
        back_populates='units'
    )
    subject: Mapped['Subject'] = relationship('Subject', back_populates='units')

    def __repr__(self):
        return f"Unit <{self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Subject(db.Model):
    __tablename__ = 'subject'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    units: Mapped[list["Unit"]] = relationship('Unit', back_populates='subject')
  
class Chapter(db.Model):
    __tablename__='chapter'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey('unit.id', name='fk_chapter_unit_id'))
    video_url: Mapped[str] = mapped_column(String(255))
    video_blurb: Mapped[str] = mapped_column(Text, nullable=True)  
    quiz_blurb: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    quiz_blurb_img_url: Mapped[str] = mapped_column(String(255), nullable = True)

    unit: Mapped["Unit"] = relationship('Unit', back_populates='chapters')
    questions: Mapped[list["Question"]] = relationship('Question', back_populates='chapter')
    topics: Mapped[list["QuestionTopic"]] = relationship('QuestionTopic', back_populates='chapter')

    users: Mapped[list["User"]] = relationship(
        'User',
        secondary=user_chapter_association,
        back_populates='chapters'
    ) 

    chapter_progress: Mapped[list["UserChapterProgress"]] = relationship('UserChapterProgress', back_populates='chapter')
    # users: Mapped[list["User"]] = relationship(
    #     'User',
    #     back_populates='current_chapter'
    # )

    
    def __repr__(self):
        return f"Chapter <{self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Question(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id', name='question_chapter_id'))
    topic_id: Mapped[int] = mapped_column(ForeignKey('question_topic.id', name='question_topic_id'))
    image_url: Mapped[str] = mapped_column(Text, nullable=True)

    chapter: Mapped["Chapter"] = relationship('Chapter', back_populates='questions')
    topic: Mapped["QuestionTopic"] = relationship('QuestionTopic', back_populates='questions')
    answers: Mapped[list["Answer"]] = relationship('Answer', back_populates='question')
    

    def __repr__(self):
        return f"Question <{self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

class QuestionTopic(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'))

    questions: Mapped[list["Question"]] = relationship('Question', back_populates='topic')
    chapter: Mapped["Chapter"] = relationship('Chapter', back_populates='topics')

    user_progresses: Mapped[list['UserTopicProgress']] = relationship('UserTopicProgress', back_populates='topic')
    
    def __repr__(self):
        return f"Topic <{self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

class Answer(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id', name='answer_question_id'))
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    question: Mapped["Question"] = relationship('Question', back_populates='answers')

    def save(self):
        db.session.add(self)
        db.session.commit()

class UserPerformance(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', name='userperformance_user_id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id', name='userperformance_qusetion_id'))
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='performances')

    def save(self):
        db.session.add(self)
        db.session.commit()

class UserChapterProgress(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', name='user_chapter_progress_id'), nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id', name='chapter_progress_user_id'), nullable=False)
    video_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    quiz_grade: Mapped[int] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default = True, nullable=True)
    # completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'chapter_id', name='uix_user_chapter'),)
    
    user = relationship('User', back_populates='chapter_progress')
    chapter = relationship('Chapter')

    def __repr__(self):
        return f"Progress for user<{self.user_id}> on video in chapter {self.chapter_id}"


class UserTopicProgress(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', name='user_topic_progress_id'), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey('question_topic.id', name='topic_progress_user_id'), nullable=False)
    questions_asked: Mapped[int] = mapped_column(Integer, default=0)
    answered_correctly: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (db.UniqueConstraint('user_id', 'topic_id', name='uix_user_topic'),)

    user = relationship('User', back_populates='topic_progresses')
    topic = relationship('QuestionTopic', back_populates = 'user_progresses')
