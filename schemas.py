from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    user_id: int

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    user_id: int
    class Config:
        from_attributes = True