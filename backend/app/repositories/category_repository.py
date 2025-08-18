from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .base import BaseRepository
from ..models.category import Category
from ..models.note import Note, note_categories


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model with specific business logic"""
    
    def __init__(self, db: Session):
        super().__init__(db, Category)
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name"""
        return self.db.query(Category).filter(Category.name == name).first()
    
    def get_with_notes_count(self) -> List[tuple[Category, int]]:
        """Get all categories with their notes count"""
        return (
            self.db.query(Category, func.count(note_categories.c.note_id).label('notes_count'))
            .outerjoin(note_categories, Category.id == note_categories.c.category_id)
            .group_by(Category.id)
            .order_by(Category.name)
            .all()
        )
    
    def get_categories_by_ids(self, category_ids: List[int]) -> List[Category]:
        """Get multiple categories by their IDs"""
        return (
            self.db.query(Category)
            .filter(Category.id.in_(category_ids))
            .all()
        )
    
    def search_by_name(self, search_term: str) -> List[Category]:
        """Search categories by name (case insensitive)"""
        return (
            self.db.query(Category)
            .filter(Category.name.ilike(f"%{search_term}%"))
            .order_by(Category.name)
            .all()
        )