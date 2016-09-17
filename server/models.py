from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

class GameState(db.Model):
    __tablename__ = 'game_state'

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer, db.ForeignKey('session.id'))
    json = db.Column(JSON)

    def __init__(self, json):
        self.json = json

    def __repr__(self):
        return '<id {}>'.format(self.id)

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