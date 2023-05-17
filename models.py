from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    emails = db.relationship('Email', backref='user', lazy=True, cascade="all, delete-orphan")
    phoneNumbers = db.relationship('PhoneNumber', backref='user', lazy=True, cascade="all, delete-orphan")


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return str(self.mail)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return str(self.number)