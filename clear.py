"""
Clear duplicate or problematic events
"""

from database.connection import SessionLocal
from database.models import CalendarEvent
from datetime import datetime

db = SessionLocal()

# Get all events
events = db.query(CalendarEvent).all()

print(f"\n📊 Total events: {len(events)}")

# Find and delete problematic events (longer than 24 hours)
deleted = 0
for event in events:
    duration = (event.end_time - event.start_time).total_seconds() / 3600
    if duration > 24:
        print(f"❌ Deleting long event: {event.title} ({duration:.1f} hours)")
        db.delete(event)
        deleted += 1

if deleted > 0:
    db.commit()
    print(f"\n✅ Deleted {deleted} problematic events")
else:
    print("\n✅ No problematic events found")

# Show remaining events
remaining = db.query(CalendarEvent).all()
print(f"\n📋 Remaining events: {len(remaining)}")
for e in remaining:
    duration = (e.end_time - e.start_time).total_seconds() / 3600
    print(f"  - {e.title}: {e.start_time.strftime('%Y-%m-%d %H:%M')} ({duration:.1f}h)")

db.close()