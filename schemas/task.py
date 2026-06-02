"""
Pydantic Schemas for Task
"""

from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int
    deadline: str

class TaskUpdate(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    assigned_to: int
    deadline: datetime
    status: str
    created_at: datetime
    updated_at: datetime