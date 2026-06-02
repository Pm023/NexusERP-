"""
Pydantic Schemas for Manufacturer
"""

from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class ManufacturerBase(BaseModel):
    name: str
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    gst_number: Optional[str] = None
    product_category: Optional[str] = None
    is_active: bool = True

class ManufacturerCreate(ManufacturerBase):
    pass

class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    gst_number: Optional[str] = None
    product_category: Optional[str] = None
    is_active: Optional[bool] = None

class ManufacturerResponse(ManufacturerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)