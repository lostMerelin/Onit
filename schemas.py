from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

from pydantic import BaseModel, ConfigDict

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

from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)