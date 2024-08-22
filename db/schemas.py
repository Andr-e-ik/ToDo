from pydantic import BaseModel

class TaskItemBase(BaseModel):
    title: str
    description: str = ""
    status: bool = False

class TaskItemCreate(TaskItemBase):
    pass

class TaskItemUpdate(TaskItemBase):
    pass

class TaskItem(TaskItemBase):
    id: int

    class Config:
        orm_mode = True


