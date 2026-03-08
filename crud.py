from sqlalchemy.orm import Session
from sqlalchemy import select
if __package__:
    from . import models, schemas
else:
    import models, schemas

def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(name=data.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session) -> list[models.User]:
    return list(db.scalars(select(models.User)).all())

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(title=data.title, user_id=data.user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_tasks(db: Session) -> list[models.Task]:
    return list(db.scalars(select(models.Task)).all())

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)

def update_task(db: Session, task: models.Task, data: schemas.TaskUpdate) -> models.Task:
    if data.title is not None:
        task.title = data.title
    if data.done is not None:
        task.done = data.done
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
