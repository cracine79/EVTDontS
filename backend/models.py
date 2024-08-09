from exts import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, text

class Base(DeclarativeBase):
    pass

"""
    class: User
    id: integer
    email: string
    password: string
"""

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password_hash: Mapped[str]

    def __repr__(self):
        return f"User <{self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()