import os
import json
from sqlalchemy import Column, String, create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


database_name = 'agency'
db = SQLAlchemy()
database_path = os.getenv('DATABASE_URL')
local_db = 'postgres://noura.@localhost:5432/agency'

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.secret_key = os.getenv('SECRET')


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release = Column(db.DateTime(), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, title, release):
        self.title = title
        self.release = release

    def __repr__(self):
        return json.dumps(self.format())

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release
        }


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return json.dumps(self.format())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
