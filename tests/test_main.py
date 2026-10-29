from fastapi.testclient import TestClient
from database import Base, engine
import main

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(main.app)

def test_create_task():
    r = client.post("/tasks", json={"title": "Prepare report", "assigned_to": "ana@example.com"})
    assert r.status_code == 201
    assert r.json()["title"] == "Prepare report"

def test_mark_done():
    tid = client.post("/tasks", json={"title": "Call client"}).json()["id"]
    r = client.patch(f"/tasks/{tid}/done")
    assert r.status_code == 200 and r.json()["done"] is True

def test_missing_task_is_404():
    assert client.patch("/tasks/99999/done").status_code == 404

