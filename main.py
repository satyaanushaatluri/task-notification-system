"""Task & Notification System - FastAPI + SQLAlchemy.
Notifications run as background tasks so the API response is not slowed down.
For production, move send_notification to Celery workers and add real email/SMTP.
Run: pip install -r requirements.txt && uvicorn main:app --reload
"""
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from database import Base, engine, get_db
from models import Task

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task & Notification System")

class TaskIn(BaseModel):
    title: str
    assigned_to: Optional[str] = None

class TaskOut(TaskIn):
    id: int
    done: bool
    notification_status: str

def to_out(t: Task) -> TaskOut:
    return TaskOut(id=t.id, title=t.title, assigned_to=t.assigned_to,
                   done=t.done, notification_status=t.notification_status)

def send_notification(task_id: int):
    """Simulated sender: in production replace the print with SMTP/messaging.
    It runs in the background and records the result in the database."""
    db = next(get_db())
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task and task.assigned_to:
            print(f"Notification: task {task.id} '{task.title}' -> {task.assigned_to}")
            task.notification_status = "sent"
            db.commit()
        elif task:
            task.notification_status = "failed"
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Task & Notification System is running"}

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return [to_out(t) for t in db.query(Task).all()]

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(data: TaskIn, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task = Task(title=data.title, assigned_to=data.assigned_to)
    db.add(task); db.commit(); db.refresh(task)
    if task.assigned_to:
        background_tasks.add_task(send_notification, task.id)
    return to_out(task)

@app.patch("/tasks/{task_id}/done", response_model=TaskOut)
def mark_done(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True; db.commit()
    return to_out(task)

@app.post("/tasks/{task_id}/retry-notification", response_model=TaskOut)
def retry_notification(task_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    background_tasks.add_task(send_notification, task.id)
    return to_out(task)

