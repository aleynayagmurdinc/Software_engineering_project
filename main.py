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


@app.post("/courses")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = models.Course(
        code=course.code,
        title=course.title
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@app.post("/activities")
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    try:
        new_activity = models.Activity(
            course_id=activity.course_id,
            activity_number=activity.activity_number,
            title=activity.title,
            text=activity.text,
            status="NOT_STARTED",
            created_by="11111111-1111-1111-1111-111111111111"
        )

        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)

        return new_activity

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}



@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    activities = db.query(models.Activity).all()
    return activities

print("REGISTERED ROUTES:")
for route in app.routes:
    print(route.path)
