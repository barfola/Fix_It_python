from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'Users'

    uuid = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    adminLevel = db.Column(db.Integer, nullable=False)
    hashPassword = db.Column(db.Text, nullable=False)


class Reports(db.Model):
    __tablename__ = 'Reports'

    uuid = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Integer, nullable=False)
    reportType = db.Column(db.Integer, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)