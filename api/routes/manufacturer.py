import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from database.models import Manufacturer
from schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate, ManufacturerResponse
from utils.storage import save_to_drive, update_drive_file, delete_from_drive, get_all_files, MANUFACTURER_DRIVE

router = APIRouter()

@router.post("", response_model=ManufacturerResponse, status_code=201)
def create_manufacturer(manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):
    """Create new manufacturer"""
    
    db_mfr = Manufacturer(**manufacturer.model_dump())
    db.add(db_mfr)
    db.commit()
    db.refresh(db_mfr)
    
    # Save to drive
    mfr_dict = {
        'id': db_mfr.id,
        'name': db_mfr.name,
        'company_name': db_mfr.company_name,
        'email': db_mfr.email,
        'phone': db_mfr.phone,
        'address': db_mfr.address,
        'city': db_mfr.city,
        'state': db_mfr.state,
        'country': db_mfr.country,
        'gst_number': db_mfr.gst_number,
        'product_category': db_mfr.product_category,
        'is_active': db_mfr.is_active,
        'created_at': str(db_mfr.created_at),
        'updated_at': str(db_mfr.updated_at)
    }
    save_to_drive(MANUFACTURER_DRIVE, f"manufacturer_{db_mfr.id}", mfr_dict)
    
    return db_mfr

@router.get("", response_model=List[ManufacturerResponse])
def get_manufacturers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    city: Optional[str] = None,
    product: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all manufacturers with filters"""
    
    query = db.query(Manufacturer)
    
    if city:
        query = query.filter(Manufacturer.city.ilike(f"%{city}%"))
    
    if product:
        query = query.filter(Manufacturer.product_category.ilike(f"%{product}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/{manufacturer_id}", response_model=ManufacturerResponse)
def get_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    """Get specific manufacturer"""
    
    db_mfr = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not db_mfr:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return db_mfr

@router.put("/{manufacturer_id}", response_model=ManufacturerResponse)
def update_manufacturer(manufacturer_id: int, manufacturer: ManufacturerUpdate, db: Session = Depends(get_db)):
    """Update manufacturer"""
    
    db_mfr = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not db_mfr:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    
    # Update fields
    update_data = manufacturer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mfr, field, value)
    
    db_mfr.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_mfr)
    
    # Update drive file
    mfr_dict = {
        'id': db_mfr.id,
        'name': db_mfr.name,
        'company_name': db_mfr.company_name,
        'email': db_mfr.email,
        'phone': db_mfr.phone,
        'address': db_mfr.address,
        'city': db_mfr.city,
        'state': db_mfr.state,
        'country': db_mfr.country,
        'gst_number': db_mfr.gst_number,
        'product_category': db_mfr.product_category,
        'is_active': db_mfr.is_active,
        'created_at': str(db_mfr.created_at),
        'updated_at': str(db_mfr.updated_at)
    }
    update_drive_file(MANUFACTURER_DRIVE, f"manufacturer_{manufacturer_id}", mfr_dict)
    
    return db_mfr

@router.delete("/{manufacturer_id}", status_code=204)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    """Delete manufacturer"""
    
    db_mfr = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not db_mfr:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    
    db.delete(db_mfr)
    db.commit()
    delete_from_drive(MANUFACTURER_DRIVE, f"manufacturer_{manufacturer_id}")
    
    return None

@router.get("/drive-info", include_in_schema=False)
def get_drive_info():
    """Get drive information"""
    import os
    files = get_all_files(MANUFACTURER_DRIVE)
    
    return {
        "status": "success",
        "drive_path": MANUFACTURER_DRIVE,
        "folder_exists": os.path.exists(MANUFACTURER_DRIVE),
        "is_writable": os.access(MANUFACTURER_DRIVE, os.W_OK) if os.path.exists(MANUFACTURER_DRIVE) else False,
        "total_files": len(files),
        "files": files
    }