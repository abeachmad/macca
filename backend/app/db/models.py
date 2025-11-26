from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    goal = Column(String)  # job_interview, study, daily_conversation
    level = Column(String)  # A1, A2, B1, B2, C1, C2
    explanation_language = Column(String, default="id")  # id, en
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    sessions = relationship("Session", back_populates="user")
    utterances = relationship("Utterance", back_populates="user")
    feedback_issues = relationship("FeedbackIssue", back_populates="user")
    vocabulary_items = relationship("VocabularyItem", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    mode = Column(String)  # live_conversation, guided_lesson, pronunciation_coach
    topic = Column(String, nullable=True)
    lesson_id = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="sessions")
    utterances = relationship("Utterance", back_populates="session")
    feedback_issues = relationship("FeedbackIssue", back_populates="session")

class Utterance(Base):
    __tablename__ = "utterances"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"))
    user_id = Column(String(36), ForeignKey("users.id"))
    role = Column(String)  # user, assistant
    audio_url = Column(String, nullable=True)
    transcript = Column(Text)
    raw_llm_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("Session", back_populates="utterances")
    user = relationship("User", back_populates="utterances")
    feedback_issues = relationship("FeedbackIssue", back_populates="utterance")

class FeedbackIssue(Base):
    __tablename__ = "feedback_issues"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    session_id = Column(String(36), ForeignKey("sessions.id"))
    utterance_id = Column(String(36), ForeignKey("utterances.id"))
    type = Column(String)  # grammar, vocabulary, pronunciation
    issue_code = Column(String)  # past_simple, articles, pronunciation_th
    detail = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="feedback_issues")
    session = relationship("Session", back_populates="feedback_issues")
    utterance = relationship("Utterance", back_populates="feedback_issues")

class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    word = Column(String)
    translation = Column(String)
    example = Column(Text)
    source = Column(String)  # conversation, lesson, manual
    strength = Column(Float, default=0.0)  # 0-1
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="vocabulary_items")