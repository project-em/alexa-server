from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from server.app import db

class GameState(db.Model):
    __tablename__ = 'game_state'

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer, db.ForeignKey('session.id'))
    json = db.Column(JSON)

    def __init__(self, json):
        self.json = json

    def __repr__(self):
        return '<id {}>'.format(self.id)