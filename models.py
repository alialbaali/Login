import jwt
from sqlalchemy import Column, String, Integer

from db import db

# User Model


# JWT Secret
# You should store the 'JWT Secret' in environment variable or somewhere safe!
JWT_SECRET = 'secret'
ALGORITHM = 'HS256'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, name, username, password):
        self.name = name,
        self.username = username,
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def generate_token(self):
        token = jwt.encode({'user_id': self.id}, JWT_SECRET, algorithm=ALGORITHM)
        return token

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username
        }
