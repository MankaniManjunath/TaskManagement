from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from models.models import Task, TaskStatus

# Pydantic schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

def create_task(db: Session, task: TaskCreate, user_id: int):
    # This function creates a new task in the database. It takes a database session,
    # a task object containing the task details, and the ID of the user who owns the task.
    # After creating the task, it adds it to the session, commits the transaction, 
    # and refreshes the task object to get the updated state from the database.
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # This function retrieves a list of tasks from the database that belong to a specific user.
    # It takes a database session, the user's ID, and optional parameters for pagination (skip and limit).
    # The function returns a list of tasks that match the criteria.
    return db.query(Task).filter(Task.owner_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int, user_id: int):
    # This function fetches a specific task from the database based on the task ID and the owner's user ID.
    # If the task is not found, it raises a 404 HTTP exception indicating that the task does not exist.
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int):
    # This function updates an existing task in the database. It first retrieves the task using the task ID
    # and the owner's user ID. If the task is found, it updates the task's attributes with the new values
    # provided in the task_update object, excluding any unset values. After updating, it commits the changes
    # to the database and refreshes the task object to reflect the updated state.
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    # This function deletes a specific task from the database. It checks if the task exists based on the task ID
    # and the owner's user ID. If the task is found, it deletes the task from the database and commits the changes.
    # It returns a success message indicating that the task has been deleted.
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}
