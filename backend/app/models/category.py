from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(7), default="#3B82F6")  # Default blue color
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with notes (many-to-many through association table)
    notes = relationship("Note", secondary="note_categories", back_populates="categories")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"