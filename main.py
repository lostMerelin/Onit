import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from db import Base, engine, get_db
import crud
import schemas
import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="ORM Lab - Tasks", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def root():
    node_name = os.getenv("NODE_NAME", "Неизвестная нода")
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Информация о ноде</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: white;
                padding: 40px 60px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            h1 {{
                margin: 0;
                font-size: 42px;
                color: #222;
            }}
            p {{
                margin-top: 16px;
                color: #666;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{node_name}</h1>
            <p>Балансировка нагрузки через Nginx (round-robin)</p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "ok", "node": os.getenv("NODE_NAME", "unknown")}


@app.post("/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)


@app.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.list_users(db)


@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    user = db.get(models.User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task(db, payload)


@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return crud.list_tasks(db)


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def patch_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, payload)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"deleted": True}