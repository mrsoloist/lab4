from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

######################## API Key from .env file
API_KEY = os.getenv("API_KEY")

######################## Dependency to verify API Key
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY") or request.query_params.get("api_key")
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key: Missing API Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

######################## Common Task Handling Functionality
def get_task_by_id(task_id: int, task_db: list):
    return next((task for task in task_db if task["task_id"] == task_id), None)

def create_task(task_db: list, task_title: str, task_desc: str):
    new_task = {"task_id": len(task_db) + 1, "task_title": task_title, "task_desc": task_desc, "is_finished": False}
    task_db.append(new_task)
    return new_task

def delete_task(task_db: list, task_id: int):
    task = get_task_by_id(task_id, task_db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db.remove(task)
    return {"status": "ok", "message": "Task deleted successfully"}

def update_task(task_db: list, task_id: int, task_title: str = None, task_desc: str = None, is_finished: bool = None):
    task = get_task_by_id(task_id, task_db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_title is not None:
        task["task_title"] = task_title
    if task_desc is not None:
        task["task_desc"] = task_desc
    if is_finished is not None:
        task["is_finished"] = is_finished
    return {"status": "ok", "task": task}

######################## Database for v1 and v2
task_db_v1 = [
    {"task_id": 1, "task_title": "Test 1", "task_desc": "Complete FastAPI basics", "is_finished": False}
]

task_db_v2 = [
    {"task_id": 1, "task_title": "Test 2", "task_desc": "Revise To-Do API", "is_finished": False}
]

######################## API v1
@app.get("/apiv1/", dependencies=[Depends(verify_api_key)])
def apiv1_root():
    return {"message": "Welcome to API v1"}

@app.get("/apiv1/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def get_task_v1(task_id: int):
    task = get_task_by_id(task_id, task_db_v1)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}

@app.post("/apiv1/tasks/", status_code=201)
def create_task_v1(task_title: str, task_desc: str, api_key: str = Depends(verify_api_key)):
    new_task = create_task(task_db_v1, task_title, task_desc)
    return {"status": "ok", "task": new_task}

@app.delete("/apiv1/tasks/{task_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_task_v1(task_id: int):
    return delete_task(task_db_v1, task_id)

@app.patch("/apiv1/tasks/{task_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def update_task_v1(task_id: int, task_title: str = None, task_desc: str = None, is_finished: bool = None):
    return update_task(task_db_v1, task_id, task_title, task_desc, is_finished)

######################## API v2
@app.get("/apiv2/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def get_task_v2(task_id: int):
    task = get_task_by_id(task_id, task_db_v2)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}

@app.post("/apiv2/tasks/", status_code=201, dependencies=[Depends(verify_api_key)])
def create_task_v2(task_title: str, task_desc: str):
    new_task = create_task(task_db_v2, task_title, task_desc)
    return {"status": "ok", "task": new_task}

@app.delete("/apiv2/tasks/{task_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_task_v2(task_id: int):
    return delete_task(task_db_v2, task_id)

@app.patch("/apiv2/tasks/{task_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def update_task_v2(task_id: int, task_title: str = None, task_desc: str = None, is_finished: bool = None):
    return update_task(task_db_v2, task_id, task_title, task_desc, is_finished)
