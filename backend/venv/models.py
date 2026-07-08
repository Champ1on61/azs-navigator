from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from datetime import datetime
from database import Base

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lat = Column(Float)
    lng = Column(Float)
    amenities = Column(JSON, default={})
    fuels = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, index=True)
    author_name = Column(String, default='Гость')
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class RoadEvent(Base):
    __tablename__ = 'road_events'
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    type = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class HelpRequest(Base):
    __tablename__ = 'help_requests'
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lng = Column(Float)
    type = Column(String)
    contact = Column(String)
    comment = Column(String)
    status = Column(String, default='new')
    created_at = Column(DateTime, default=datetime.utcnow)