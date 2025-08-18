from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .category import CategoryResponse


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")


class NoteCreate(NoteBase):
    category_ids: List[int] = Field(default_factory=list, description="List of category IDs")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    is_archived: Optional[bool] = None
    category_ids: Optional[List[int]] = None


class NoteResponse(NoteBase):
    id: int
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