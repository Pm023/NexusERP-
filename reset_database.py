"""
Run this file to reset database
"""

import os
from database.connection import engine, Base
from database.models import Admin, Buyer, Manufacturer, Task

# Delete old database
if os.path.exists("unified.db"):
    os.remove("unified.db")
    print("[+] Old database deleted")

# Create all tables fresh
Base.metadata.create_all(bind=engine)
print("[+] New database created with all tables")

# Now setup admins
from database.connection import SessionLocal
from utils.auth import ADMIN_CREDENTIALS

db = SessionLocal()

try:
    for username, data in ADMIN_CREDENTIALS.items():
        admin = Admin(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"],
            is_active=True
        )
        db.add(admin)
        print(f"[+] Added: {data['full_name']} ({username})")
    
    db.commit()
    print("\n[OK] All 3 admins created successfully!")
    
    # Show all admins
    admins = db.query(Admin).all()
    print(f"\n[-] Total admins in database: {len(admins)}")
    for a in admins:
        print(f"   - {a.full_name} ({a.username}) - ID: {a.id}")

except Exception as e:
    db.rollback()
    print(f"[ERROR] Error: {e}")

finally:
    db.close()