"""Starter Task & Notification System - FastAPI skeleton.
Run: pip install -r requirements.txt && uvicorn main:app --reload
Notifications use FastAPI BackgroundTasks in this starter.
For production, move them to Celery workers with retry logic.
"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Task & Notification System (Starter)")

class Task(BaseModel):
    id: int
    title: str
    assigned_to: Optional[str] = None
    done: bool = False
    notification_status: str = "pending"

tasks: List[Task] = []

def send_notification(task: Task):
    # Starter version: log instead of sending a real email.
    # Replace this with your email/SMTP or messaging sender.
    print(f"Notification for task {task.id}: {task.title} -> {task.assigned_to}")
    task.notification_status = "sent"

@app.get("/")
def root():
    return {"message": "Task & Notification System starter is running"}

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task, background_tasks: BackgroundTasks):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task id already exists")
    tasks.append(task)
    if task.assigned_to:
        background_tasks.add_task(send_notification, task)
    return task

@app.patch("/tasks/{task_id}/done", response_model=Task)
def mark_done(task_id: int):
    for t in tasks:
        if t.id == task_id:
            t.done = True
            return t
    raise HTTPException(status_code=404, detail="Task not found")
