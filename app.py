from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from db.database import engine
from db import repository, schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.post("/todos", response_model=schemas.TaskItem)
async def create_task(title: str = Form(...), description: str = Form("")):
    async with AsyncSession(engine) as session:
        await repository.create_task(session, title, description)
    return RedirectResponse(url="/", status_code=303)


@app.get("/todos/", response_model=List[schemas.TaskItem])
async def read_todos():
    async with AsyncSession(engine) as session:
        tasks = await repository.read_todos(session)
    return tasks


@app.post("/todos/{todo_id}")
async def update_todo(todo_id: int):
    async with AsyncSession(engine) as session:
        task = await repository.update_todo(todo_id, session)
        if task is None:
            raise HTTPException(status_code=404, detail="Todo not found")
    return RedirectResponse(url="/", status_code=303)


@app.post("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int):
    async with AsyncSession(engine) as session:
        status = await repository.delete_todo(todo_id, session)
        if status is False:
            raise HTTPException(status_code=404, detail="Todo not found")
    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def get_todo_page(request: Request):
    async with AsyncSession(engine) as session:
        tasks = await repository.read_todos(session)
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": tasks})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
