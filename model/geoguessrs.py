from random import randrange
from datetime import date, time
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Geoguessr(db.Model):
    __tablename__ = 'geoguessr'

    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=False, nullable=False)
    _score = db.Column(db.String(255), unique=False, nullable=False)
    _stopwatch = db.Column(db.String(255), unique=False, nullable=False)
    _dos = db.Column(db.Date)

    def __init__(self, username="none", score='0', stopwatch='00:00:00', dos=date.today()):
        self._username = username
        self._score = score
        self._stopwatch = stopwatch
        self._dos = dos

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        self._username = username

    @property
    def score(self):
        return self._score
    
    # Setter function
    @score.setter
    def score(self, score):
        self._score = score

    @property
    def stopwatch(self):
        return self._stopwatch
    
    @stopwatch.setter
    def stopwatch(self, stopwatch):
        self._stopwatch = stopwatch
    
    # Convert dos to a string
    @property
    def dos(self):
        dos_string = self._dos.strftime('%m-%d-%Y')
        return dos_string
    
    # Setter function
    @dos.setter
    def dos(self, dos):
        self._dos = dos
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    def update(self, username="", score="", stopwatch=""):
        if len(username) > 0:
            self.username = username
        if len(score) > 0:
            self.score = score
        if len(stopwatch) > 0:
            self.stopwatch = stopwatch
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def make_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "score": self.score,
            "stopwatch": self.stopwatch,
            "dos": self.dos
        }

def initGeoguessr():
    with app.app_context():
        db.create_all()
        users = [
        Geoguessr(username='Evan', score='500', stopwatch='00:15:30', dos=date(2023, 1, 22)),
        Geoguessr(username='Max', score='650', stopwatch='00:10:45', dos=date(2023, 1, 21)),
        Geoguessr(username='Kalani', score='0', stopwatch='00:05:20', dos=date(2023, 1, 20)),
        Geoguessr(username='Nathan', score='650', stopwatch='00:12:40', dos=date(2023, 1, 19)),
        Geoguessr(username='Jaden', score='1100', stopwatch='00:25:10', dos=date(2023, 1, 22))
        ]

        for user in users:
            try:
                user.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist or duplicate data: {user.username}")

