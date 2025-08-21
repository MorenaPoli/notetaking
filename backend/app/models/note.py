from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

# Association table for many-to-many relationship between notes and categories
note_categories = Table(
    'note_categories',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class NoteType(str, enum.Enum):
    NOTE = "note"
    TODO = "todo"

class TodoStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    note_type = Column(Enum(NoteType), default=NoteType.NOTE, index=True)
    todo_status = Column(Enum(TodoStatus), default=TodoStatus.PENDING, index=True)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    is_archived = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with categories (many-to-many)
    categories = relationship("Category", secondary=note_categories, back_populates="notes")
    
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', type={self.note_type}, archived={self.is_archived})>"