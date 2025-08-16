from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ModerationRequest(Base):
    __tablename__ = "moderation_requests"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String)
    content_hash = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    results = relationship("ModerationResult", back_populates="request")

class ModerationResult(Base):
    __tablename__ = "moderation_results"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"))
    classification = Column(String)
    confidence = Column(Integer)
    reasoning = Column(String)
    llm_response = Column(String)

    request = relationship("ModerationRequest", back_populates="results")

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"))
    channel = Column(String)
    status = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
