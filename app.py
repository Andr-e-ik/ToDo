from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from database import get_db
from models import TaskItem
import schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.post("/todos", response_model=schemas.TaskItem)
async def create_task(title: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    new_task = TaskItem(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return RedirectResponse(url="/", status_code=303)

@app.get("/todos/", response_model=List[schemas.TaskItem])
def read_todos(db: Session = Depends(get_db)):
    tasks = db.query(TaskItem).all()
    return tasks

@app.post("/todos/{todo_id}")
async def update_todo(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskItem).filter(TaskItem.id == todo_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    task.status = not task.status
    db.commit()
    db.refresh(task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/delete/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskItem).filter(TaskItem.id == todo_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(task)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def get_todo_page(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(TaskItem).all()
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": tasks})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
