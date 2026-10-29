# Task and Notification System

FastAPI + SQLAlchemy project for tasks and notifications.

## What it does
- Creates tasks and assigns them to a user
- Sends notifications as background tasks, so API responses stay fast
- Records notification status (`pending` / `sent` / `failed`) in the database
- Retries a failed notification

## Run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Tests
```bash
pytest
```

## Next step for production
Move `send_notification` to Celery workers and replace the print with a real email/SMTP sender.

