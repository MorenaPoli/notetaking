from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum
from .category import CategoryResponse


class NoteType(str, Enum):
    NOTE = "note"
    TODO = "todo"

class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")
    note_type: NoteType = Field(default=NoteType.NOTE, description="Type of note")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    due_date: Optional[datetime] = Field(None, description="Due date for todos")


class NoteCreate(NoteBase):
    category_ids: List[int] = Field(default_factory=list, description="List of category IDs")
    todo_status: TodoStatus = Field(default=TodoStatus.PENDING, description="Todo status")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    note_type: Optional[NoteType] = None
    todo_status: Optional[TodoStatus] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    is_archived: Optional[bool] = None
    category_ids: Optional[List[int]] = None


class NoteResponse(NoteBase):
    id: int
    todo_status: TodoStatus
    is_archived: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True


class NoteListResponse(BaseModel):
    notes: List[NoteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int