from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)