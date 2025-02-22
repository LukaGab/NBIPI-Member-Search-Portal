from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    member_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)

    def __repr__(self):
        return f'<Member {self.member_number}: {self.last_name}, {self.first_name}>'

    def to_dict(self):
        return {
            'member_number': self.member_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }