from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    verified = db.Column(db.String(80), nullable=True)

    def __init__(self, username, email, password, verified=None):
        self.username = username
        self.email = email
        self.password = password
        self.verified = verified

    def __str__(self):
        return f'{self.username} by {self.email}'

    def __repr__(self):
        return f'{self.username}, {self.email}'

    def json(self):
        return {'username': self.username, 'email': self.email}
