from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.connection import get_db
from controller.authController import get_current_active_user
from controller.taskController import (
    TaskResponse, TaskCreate, TaskUpdate,
    create_task, get_tasks, get_task, update_task, delete_task
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse)
def create_new_task(
    task: TaskCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    return create_task(db=db, task=task, user_id=current_user.id)

@router.get("/", response_model=List[TaskResponse])
def read_all_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    tasks = get_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def read_one_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    return get_task(db=db, task_id=task_id, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_one_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    return update_task(
        db=db, task_id=task_id, task_update=task_update, user_id=current_user.id
    )

@router.delete("/{task_id}")
def delete_one_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_active_user)
):
    return delete_task(db=db, task_id=task_id, user_id=current_user.id)
