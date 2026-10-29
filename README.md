# Task and Notification System (Starter)

A starter FastAPI project for creating tasks, assigning users, and sending notifications.

## What it does
- Creates tasks and assigns them to a user
- Sends a notification in the background, so the API response is not slowed down
- Marks tasks as done

## Run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs

## Next steps
Move notifications to Celery workers, add retry logic for failed emails, and store delivery status in PostgreSQL.
