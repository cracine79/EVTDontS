from exts import db


"""
    class: User
    id: integer
    email: string
    password: string
"""

class User(db.Model):
    id=db.Column(db.Integer, primary_key=-True)
    username=db.Column(db.String(25), nullable=False, unique=True)
    email=db.Column(db.String(80), nullable=False) 
    password_hash=db.Column(db.Text(),nullable=False)

    def __repr__(self):
        return f"User <{self.username}>"