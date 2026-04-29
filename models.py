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
  
