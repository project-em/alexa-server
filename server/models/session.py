from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from guid import GUID
from server.app import db

class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    key = db.Column(GUID)
    host = db.Column(db.String(15))
    port = db.Column(db.Integer)
    
    def __init__(self, host, port):
        self.active = True
        self.create_date = datetime.now()
        self.host = host
        self.port = port

    def __repr__(self):
        return '<key {}>'.format(self.key)