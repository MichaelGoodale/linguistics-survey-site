from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from .db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    recordings = relationship("Recording", back_populates="user")

    def __init__(self, uuid):
        self.uuid = uuid

    def __repr__(self):
        return '<User {}, created at {}>'.format(uuid, created_at)

class Recording(Base):
    __tablename__ = 'recording'
    id = Column(Integer, primary_key=True)
    recording_name = Column(String(40), nullable=False)
    file_path = Column(String(260), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="recordings")

    def __init__(self, recording_name, file_path):
        self.recording_name = recording_name
        self.file_path = file_path
