from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    color: str = Field(default="#3B82F6", regex=r"^#[0-9A-Fa-f]{6}$", description="Hex color code")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, regex=r"^#[0-9A-Fa-f]{6}$")


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CategoryWithNotesCount(CategoryResponse):
    notes_count: int = 0