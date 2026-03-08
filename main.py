import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
import crud
import schemas

app = FastAPI(title="ORM Lab - Tasks")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)

@app.get("/users", response_model=list[schemas.UserOut])
def users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, payload)

@app.get("/tasks", response_model=list[schemas.TaskOut])
def tasks(db: Session = Depends(get_db)):
    return crud.list_tasks(db)

@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def patch_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, payload)

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"deleted": True}
