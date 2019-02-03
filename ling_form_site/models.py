from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, uuid):
        self.uuid = uuid

    def __repr__(self):
        return '<User {}, created at {}>'.format(uuid, created_at)
