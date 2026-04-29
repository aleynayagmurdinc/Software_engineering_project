import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Text, Boolean,
    ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CourseAccess(Base):
    __tablename__ = "course_access"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    access_role = Column(String, nullable=False)

    user = relationship("User")
    course = relationship("Course")


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("course_id", "activity_number", name="uq_course_activity_number"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    activity_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String, default="NOT_STARTED", nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course")
    creator = relationship("User")


class Objective(Base):
    __tablename__ = "objectives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    objective_order = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    activity = relationship("Activity")



class StudentProgress(Base):
    __tablename__ = "student_progress"
    __table_args__ = (
        UniqueConstraint("student_id", "activity_id", name="uq_student_activity_progress"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    current_step = Column(Integer, default=0)
    score = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User")
    activity = relationship("Activity")


class CoveredObjective(Base):
    __tablename__ = "covered_objectives"
    __table_args__ = (
        UniqueConstraint("student_progress_id", "objective_id", name="uq_progress_objective"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_progress_id = Column(UUID(as_uuid=True), ForeignKey("student_progress.id"), nullable=False)
    objective_id = Column(UUID(as_uuid=True), ForeignKey("objectives.id"), nullable=False)
    covered_at = Column(DateTime, default=datetime.utcnow)

    progress = relationship("StudentProgress")
    objective = relationship("Objective")


class ScoreLog(Base):
    __tablename__ = "score_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    objective_id = Column(UUID(as_uuid=True), ForeignKey("objectives.id"), nullable=True)
    score_delta = Column(Integer, nullable=False)
    metadata_json = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User")
    course = relationship("Course")
    activity = relationship("Activity")
    objective = relationship("Objective")


class ManualGrade(Base):
    __tablename__ = "manual_grades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    grade = Column(Integer, nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    instructor = relationship("User", foreign_keys=[instructor_id])
    student = relationship("User", foreign_keys=[student_id])
    activity = relationship("Activity")
  
