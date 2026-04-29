print("MAIN FILE LOADED:", __file__)


from uuid import UUID

from pydantic import BaseModel

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models

app = FastAPI(title="InClass Platform API")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CourseCreate(BaseModel):
    code: str
    title: str

class ActivityCreate(BaseModel):
    course_id: UUID
    activity_number: int
    title: str
    text: str

@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses
