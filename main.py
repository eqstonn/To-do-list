from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import engine, LocalSession
import model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (fine for local dev)
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"],
)

# THIS LINE IS THE MAGIC: It creates the tables in Postgres!
model.Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    except Exception as e:
        print(f"database error {e}")
        raise
    finally:
        db.close()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/task")
def create_task(task_name: str, db: Session = Depends(get_db)):
    new_task = model.Todo(title = task_name)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(model.Todo).all()
    return tasks

@app.get("/task/{id}")
def get_task(id: int, db: Session = Depends(get_db)):

    task = db.query(model.Todo).filter(model.Todo.id == id).first()
    if task == None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return task

@app.delete("/task/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(model.Todo).filter(model.Todo.id == id).first()
    if task == None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    db.delete(task)
    db.commit()
    return task

@app.put("/task/{id}")
def update_task(id: int, completed: bool, db: Session = Depends(get_db)):
    task = db.query(model.Todo).filter(model.Todo.id == id).first() 
    if task == None:
        raise HTTPException(status_code = 404, detail = "Task not found")
    task.completed = completed
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/search")
def search_tasks(title: str, db: Session = Depends(get_db)):
    tasks = db.query(model.Todo).filter(model.Todo.title.contains(title)).all()
    return tasks

@app.get("/tasks/stats")
def get_task_stats(db: Session = Depends(get_db)):
    tasks = db.query(model.Todo).count()
    completed_tasks = db.query(model.Todo).filter(model.Todo.completed == True).count()

    percentage = 0
    if completed_tasks > 0:
        percentage = (completed_tasks / tasks) * 100
    return {
        "total": tasks,
        "completed": completed_tasks,
        "progress_percentage": round(percentage, 2)
    }


    