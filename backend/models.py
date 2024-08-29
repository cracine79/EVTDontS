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