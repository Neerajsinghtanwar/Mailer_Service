from app.settings import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    admin = db.Column(db.Boolean, nullable=True, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'admin': self.admin,
            'timestamp': self.timestamp
        }


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('emails', lazy=True))
    is_sent = db.Column(db.Boolean, nullable=True, default=False)
    is_seen = db.Column(db.Boolean, nullable=True, default=False)
    unique_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.user.name

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.name,
            'is_sent': self.is_sent,
            'is_seen': self.is_seen,
            'uuid': self.unique_id,
            'timestamp': self.timestamp
        }


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    msg = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.user.name

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.serialize(),
            'msg': self.msg,
            'timestamp': self.timestamp
        }
