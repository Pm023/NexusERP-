from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

# Import auth
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from api.routes.auth import get_current_active_user

router = APIRouter()

# ==========================================
#  SCHEMAS (Inline - No external import needed)
# ==========================================
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None
    assigned_to: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: str
    updated_at: str

# ==========================================
#  IN-MEMORY DATABASE (No SQLAlchemy needed)
# ==========================================
tasks_db = {}
task_id_counter = 1

# ==========================================
#  ROUTES
# ==========================================

@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """Get all tasks with optional filters"""
    
    # Get all tasks
    all_tasks = list(tasks_db.values())
    
    # Apply filters
    if status_filter:
        all_tasks = [t for t in all_tasks if t["status"] == status_filter]
    
    if priority_filter:
        all_tasks = [t for t in all_tasks if t["priority"] == priority_filter]
    
    # Apply pagination
    paginated = all_tasks[skip:skip + limit]
    
    return paginated

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    """Get a specific task by ID"""
    
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return tasks_db[task_id]

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Create a new task"""
    global task_id_counter
    
    # Create task
    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "status": task.status or "pending",
        "priority": task.priority or "medium",
        "due_date": task.due_date,
        "assigned_to": task.assigned_to,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Save to database
    tasks_db[task_id_counter] = new_task
    task_id_counter += 1
    
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update an existing task"""
    
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # Get existing task
    task = tasks_db[task_id]
    
    # Update fields
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            task[field] = value
    
    task["updated_at"] = datetime.utcnow().isoformat()
    
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    """Delete a task"""
    
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    del tasks_db[task_id]
    
    return {
        "status": "success",
        "message": f"Task {task_id} deleted successfully"
    }

@router.get("/stats/summary")
async def get_task_stats(current_user: dict = Depends(get_current_active_user)):
    """Get task statistics"""
    
    all_tasks = list(tasks_db.values())
    
    stats = {
        "total": len(all_tasks),
        "by_status": {
            "pending": len([t for t in all_tasks if t["status"] == "pending"]),
            "in_progress": len([t for t in all_tasks if t["status"] == "in_progress"]),
            "completed": len([t for t in all_tasks if t["status"] == "completed"])
        },
        "by_priority": {
            "low": len([t for t in all_tasks if t["priority"] == "low"]),
            "medium": len([t for t in all_tasks if t["priority"] == "medium"]),
            "high": len([t for t in all_tasks if t["priority"] == "high"])
        }
    }
    
    return stats

# ==========================================
#  SEED DATA (Optional - for testing)
# ==========================================
def seed_tasks():
    """Create some sample tasks for testing"""
    global task_id_counter
    
    sample_tasks = [
        {
            "title": "Complete project proposal",
            "description": "Write and submit the Q1 project proposal",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2026-03-15",
            "assigned_to": "admin1"
        },
        {
            "title": "Review buyer contracts",
            "description": "Review and approve pending buyer contracts",
            "status": "pending",
            "priority": "medium",
            "due_date": "2026-03-10",
            "assigned_to": "user1"
        },
        {
            "title": "Update manufacturer database",
            "description": "Add new manufacturers to the system",
            "status": "completed",
            "priority": "low",
            "due_date": "2026-03-05",
            "assigned_to": "admin1"
        }
    ]
    
    for task_data in sample_tasks:
        tasks_db[task_id_counter] = {
            "id": task_id_counter,
            **task_data,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        task_id_counter += 1

# Seed some sample data on startup
seed_tasks()