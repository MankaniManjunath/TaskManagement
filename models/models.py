from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum as SQLAlchemyEnum
import enum
from sqlalchemy.orm import relationship
from models.connection import Base

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Define relationship with Task model
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Define relationship with User model
    owner = relationship("User", back_populates="tasks")