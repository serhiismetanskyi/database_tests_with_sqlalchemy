from datetime import datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(length=255), index=True, nullable=False)
    permissions = Column(JSON, nullable=False)
    creator_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=20), unique=True, index=True, nullable=False)
    full_name = Column(String(length=255), index=True, nullable=False)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=True)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    ipaddress = Column(String, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    registered_at = Column(DateTime(timezone=True), default=datetime.now())

    role = relationship("Role", back_populates="users")

    created_tasks = relationship("Task", foreign_keys="Task.creator_id")
    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id")


class Priority(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    priority_name = Column(String(length=255), index=True, nullable=False)
    creator_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())

    tasks = relationship("Task", back_populates="priority")


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(length=255), index=True, nullable=False)
    permissions = Column(JSON, nullable=False)
    creator_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())

    tasks = relationship("Task", back_populates="status")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=50), nullable=False)
    description = Column(String(length=255), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    priority_id = Column(
        Integer, ForeignKey("priorities.id", ondelete="CASCADE"), nullable=True
    )
    status_id = Column(
        Integer, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False
    )
    creator_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), default=datetime.now())

    priority = relationship("Priority", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")
    creator = relationship(
        "User", back_populates="created_tasks", foreign_keys="Task.creator_id"
    )
    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys="Task.assignee_id"
    )