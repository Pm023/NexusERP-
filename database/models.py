"""
Database Models - All entities in one place
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Admin(Base):
    """Admin/User model for authentication"""
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    created_tasks = relationship("Task", foreign_keys="Task.created_by", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    calendar_events = relationship("CalendarEvent", back_populates="admin")

class Buyer(Base):
    """Buyer model"""
    __tablename__ = "buyers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True, default="India", index=True)
    gst_number = Column(String(50), nullable=True)
    payment_terms = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Manufacturer(Base):
    """Manufacturer model"""
    __tablename__ = "manufacturers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    gst_number = Column(String(50), nullable=True)
    product_category = Column(String(200), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("admins.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("admins.id"), nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("Admin", foreign_keys=[created_by], back_populates="created_tasks")
    assignee = relationship("Admin", foreign_keys=[assigned_to], back_populates="assigned_tasks")

# ==================== NEW: CALENDAR EVENT MODEL ====================

class CalendarEvent(Base):
    """Calendar Event model - Simplified"""
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    
    # Basic info
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Event type: appointment, meeting, work, task, event
    event_type = Column(String(50), nullable=False, index=True)
    
    # Time
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    
    # Optional
    location = Column(String(200), nullable=True)
    
    # Status: scheduled, completed, cancelled
    status = Column(String(50), default="scheduled", index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    admin = relationship("Admin", back_populates="calendar_events")