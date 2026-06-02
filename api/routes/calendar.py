"""
Calendar Routes - Fixed Version (No Duplicate Events)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from database.connection import get_db
from database.models import CalendarEvent, Admin
from schemas.calendar import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse
from utils.auth import get_current_admin

router = APIRouter()

# ==================== CREATE EVENT (FIXED) ====================

@router.post("/events", response_model=CalendarEventResponse, status_code=201)
def create_calendar_event(
    event: CalendarEventCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new calendar event - Fixed to prevent duplicate display"""
    
    # Parse datetime - support multiple formats
    def parse_datetime(dt_str: str):
        # Remove 'T' and convert to space format
        dt_str = dt_str.replace('T', ' ')
        
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        
        raise HTTPException(
            status_code=400,
            detail=f"Invalid datetime format: {dt_str}. Use: YYYY-MM-DD HH:MM"
        )
    
    try:
        start_time = parse_datetime(event.start_time)
        end_time = parse_datetime(event.end_time)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing datetime: {str(e)}")
    
    # Validate times
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    # Prevent events longer than 24 hours (causes display issues)
    if (end_time - start_time).total_seconds() > 24 * 3600:
        raise HTTPException(
            status_code=400,
            detail="Events cannot be longer than 24 hours. Please create separate events."
        )
    
    # Create event
    db_event = CalendarEvent(
        admin_id=current_admin.id,
        title=event.title,
        event_type=event.event_type,
        start_time=start_time,
        end_time=end_time,
        description=event.description,
        location=event.location,
        status="scheduled"
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    print(f"[+] Event created: {db_event.title} | {start_time} to {end_time}")
    
    return db_event

# ==================== GET EVENTS FOR FULLCALENDAR (FIXED) ====================

@router.get("/events/fullcalendar")
def get_events_fullcalendar(
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get events in FullCalendar format - Fixed to show proper time slots"""
    
    query = db.query(CalendarEvent).filter(CalendarEvent.admin_id == current_admin.id)
    
    if start:
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            query = query.filter(CalendarEvent.start_time >= start_dt)
        except:
            pass
    
    if end:
        try:
            end_dt = datetime.strptime(end, "%Y-%m-%d")
            query = query.filter(CalendarEvent.start_time <= end_dt)
        except:
            pass
    
    events = query.all()
    
    # Color mapping
    colors = {
        "appointment": "#3788d8",
        "meeting": "#f59e0b",
        "work": "#10b981",
        "task": "#ef4444",
        "event": "#8b5cf6"
    }
    
    calendar_events = []
    
    for e in events:
        # Format datetime properly for FullCalendar
        # Make sure timezone is consistent
        start_iso = e.start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_iso = e.end_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        event_data = {
            "id": str(e.id),  # Convert to string for FullCalendar
            "title": e.title,
            "start": start_iso,
            "end": end_iso,
            "allDay": False,  # ← IMPORTANT: Never all-day
            "backgroundColor": colors.get(e.event_type, "#3788d8"),
            "borderColor": colors.get(e.event_type, "#3788d8"),
            "textColor": "#ffffff",
            "extendedProps": {
                "description": e.description,
                "event_type": e.event_type,
                "location": e.location,
                "status": e.status
            }
        }
        
        calendar_events.append(event_data)
    
    return calendar_events

# ==================== REST OF THE ROUTES (Same as before) ====================

@router.get("/events", response_model=List[CalendarEventResponse])
def get_calendar_events(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all calendar events"""
    
    query = db.query(CalendarEvent).filter(CalendarEvent.admin_id == current_admin.id)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(CalendarEvent.start_time >= start)
        except:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(CalendarEvent.end_time <= end)
        except:
            pass
    
    if event_type:
        query = query.filter(CalendarEvent.event_type == event_type.lower())
    
    events = query.order_by(CalendarEvent.start_time).all()
    return events

@router.get("/events/{event_id}", response_model=CalendarEventResponse)
def get_calendar_event(
    event_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get specific event"""
    
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.admin_id == current_admin.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event

@router.put("/events/{event_id}", response_model=CalendarEventResponse)
def update_calendar_event(
    event_id: int,
    event_update: CalendarEventUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update event"""
    
    db_event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.admin_id == current_admin.id
    ).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event_update.model_dump(exclude_unset=True)
    
    # Parse datetime if provided
    if 'start_time' in update_data:
        try:
            dt_str = update_data['start_time'].replace('T', ' ')
            update_data['start_time'] = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except:
            raise HTTPException(status_code=400, detail="Invalid start_time format")
    
    if 'end_time' in update_data:
        try:
            dt_str = update_data['end_time'].replace('T', ' ')
            update_data['end_time'] = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except:
            raise HTTPException(status_code=400, detail="Invalid end_time format")
    
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db_event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.delete("/events/{event_id}", status_code=204)
def delete_calendar_event(
    event_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete event"""
    
    db_event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.admin_id == current_admin.id
    ).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    
    return None

@router.get("/events/today/list")
def get_today_events(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get today's events"""
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    events = db.query(CalendarEvent).filter(
        CalendarEvent.admin_id == current_admin.id,
        CalendarEvent.start_time >= today_start,
        CalendarEvent.start_time < today_end,
        CalendarEvent.status == "scheduled"
    ).order_by(CalendarEvent.start_time).all()
    
    return {
        "status": "success",
        "date": today_start.strftime("%Y-%m-%d"),
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "event_type": e.event_type,
                "start_time": e.start_time.strftime("%H:%M"),
                "end_time": e.end_time.strftime("%H:%M"),
                "location": e.location
            }
            for e in events
        ]
    }

@router.get("/events/upcoming/list")
def get_upcoming_events(
    days: int = Query(7, ge=1, le=30),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get upcoming events"""
    
    now = datetime.now()
    future = now + timedelta(days=days)
    
    events = db.query(CalendarEvent).filter(
        CalendarEvent.admin_id == current_admin.id,
        CalendarEvent.start_time >= now,
        CalendarEvent.start_time <= future,
        CalendarEvent.status == "scheduled"
    ).order_by(CalendarEvent.start_time).all()
    
    return {
        "status": "success",
        "total": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "event_type": e.event_type,
                "start_time": e.start_time.isoformat(),
                "location": e.location
            }
            for e in events
        ]
    }