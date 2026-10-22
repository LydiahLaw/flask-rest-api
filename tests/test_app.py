import copy

import pytest

import app as app_module

ORIGINAL_TASKS = copy.deepcopy(app_module.tasks)


@pytest.fixture
def client():
    # Reset the in-memory store before each test so tests don't affect each other
    app_module.tasks[:] = copy.deepcopy(ORIGINAL_TASKS)
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy"}


def test_get_all_tasks(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()["tasks"]) == 2


def test_get_single_task(client):
    res = client.get("/tasks/1")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Set up EC2"


def test_get_missing_task_returns_404(client):
    res = client.get("/tasks/999")
    assert res.status_code == 404
    assert "error" in res.get_json()


def test_create_task(client):
    res = client.post("/tasks", json={"title": "Write CI pipeline"})
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "Write CI pipeline"
    assert body["done"] is False


def test_create_task_without_title_returns_400(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400


def test_delete_task(client):
    res = client.delete("/tasks/1")
    assert res.status_code == 200
    assert client.get("/tasks/1").status_code == 404


def test_delete_missing_task_returns_404(client):
    res = client.delete("/tasks/999")
    assert res.status_code == 404
