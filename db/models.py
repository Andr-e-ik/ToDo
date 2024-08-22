from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class TaskItem(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    status = Column(Boolean, default=False)
