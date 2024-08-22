from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import TaskItem


async def create_task(db: AsyncSession, title: str, description: str) -> TaskItem:
    new_task = TaskItem(title=title, description=description)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def read_todos(db: AsyncSession) -> List[TaskItem]:
    tasks = await db.execute(select(TaskItem))
    return list(tasks.scalars())


async def update_todo(todo_id: int, db: AsyncSession):
    result = await db.execute(select(TaskItem).filter(TaskItem.id == todo_id))
    task = result.scalar_one_or_none()
    if task is not None:
        task.status = not task.status
        await db.commit()
        await db.refresh(task)
        return task
    return None


async def delete_todo(todo_id: int, db: AsyncSession) -> bool:
    result = await db.execute(select(TaskItem).filter(TaskItem.id == todo_id))
    task = result.scalar_one_or_none()
    if task is not None:
        await db.delete(task)
        await db.commit()
        return True
    return False
