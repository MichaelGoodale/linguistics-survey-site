import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from .db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    responses = relationship("SurveyResponse", back_populates="user")
    consent = Column(Text)

    def __init__(self, uuid):
        self.uuid = uuid
        self.consent = ""

    def __repr__(self):
        return '<User {}, created at {}>'.format(uuid, created_at)

class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    survey_name = Column(String(40), unique=True, nullable=False)
    survey = Column(Text)
    responses = relationship("SurveyResponse", back_populates="survey")

    def __init__(self, survey_name, survey):
        self.survey_name = survey_name
        self.survey = survey


class SurveyResponse(Base):
    __tablename__ = 'response'
    id = Column(Integer, primary_key=True)
    response = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    submitted_at = Column(DateTime)
    user = relationship("User", back_populates="responses")
    survey_id = Column(Integer, ForeignKey('survey.id'))
    survey = relationship("Survey", back_populates="responses")
    __table_args__ = (UniqueConstraint('user_id', 'survey_id', name='_survey_user_uc'),)

    def __init__(self, response):
        self.response = response
