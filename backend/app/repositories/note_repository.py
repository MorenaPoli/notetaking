from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc
from .base import BaseRepository
from ..models.note import Note, note_categories
from ..models.category import Category


class NoteRepository(BaseRepository[Note]):
    """Repository for Note model with specific business logic"""
    
    def __init__(self, db: Session):
        super().__init__(db, Note)
    
    def get_by_id_with_categories(self, id: int) -> Optional[Note]:
        """Get note by ID with its categories loaded"""
        return (
            self.db.query(Note)
            .options(joinedload(Note.categories))
            .filter(Note.id == id)
            .first()
        )
    
    def get_active_notes(
        self, 
        skip: int = 0, 
        limit: int = 100,
        category_ids: Optional[List[int]] = None
    ) -> List[Note]:
        """Get active (non-archived) notes with optional category filtering"""
        query = (
            self.db.query(Note)
            .options(joinedload(Note.categories))
            .filter(Note.is_archived == False)
        )
        
        # Filter by categories if provided
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return (
            query
            .order_by(desc(Note.updated_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_archived_notes(
        self, 
        skip: int = 0, 
        limit: int = 100,
        category_ids: Optional[List[int]] = None
    ) -> List[Note]:
        """Get archived notes with optional category filtering"""
        query = (
            self.db.query(Note)
            .options(joinedload(Note.categories))
            .filter(Note.is_archived == True)
        )
        
        # Filter by categories if provided
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return (
            query
            .order_by(desc(Note.updated_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_active_notes(self, category_ids: Optional[List[int]] = None) -> int:
        """Count active notes with optional category filtering"""
        query = self.db.query(Note).filter(Note.is_archived == False)
        
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return query.count()
    
    def count_archived_notes(self, category_ids: Optional[List[int]] = None) -> int:
        """Count archived notes with optional category filtering"""
        query = self.db.query(Note).filter(Note.is_archived == True)
        
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return query.count()
    
    def search_notes(
        self, 
        search_term: str, 
        include_archived: bool = False,
        category_ids: Optional[List[int]] = None
    ) -> List[Note]:
        """Search notes by title or content"""
        query = (
            self.db.query(Note)
            .options(joinedload(Note.categories))
            .filter(
                or_(
                    Note.title.ilike(f"%{search_term}%"),
                    Note.content.ilike(f"%{search_term}%")
                )
            )
        )
        
        if not include_archived:
            query = query.filter(Note.is_archived == False)
        
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return query.order_by(desc(Note.updated_at)).all()
    
    def archive_note(self, id: int) -> Optional[Note]:
        """Archive a note"""
        note = self.get_by_id(id)
        if note:
            note.is_archived = True
            self.db.commit()
            self.db.refresh(note)
        return note
    
    def unarchive_note(self, id: int) -> Optional[Note]:
        """Unarchive a note"""
        note = self.get_by_id(id)
        if note:
            note.is_archived = False
            self.db.commit()
            self.db.refresh(note)
        return note
    
    def get_todos(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_ids: Optional[List[int]] = None
    ) -> List[Note]:
        """Get todos with optional filtering"""
        from ..models.note import NoteType, TodoStatus, Priority
        
        query = (
            self.db.query(Note)
            .options(joinedload(Note.categories))
            .filter(Note.note_type == NoteType.TODO)
            .filter(Note.is_archived == False)
        )
        
        # Filter by status if provided
        if status:
            query = query.filter(Note.todo_status == TodoStatus(status))
        
        # Filter by priority if provided
        if priority:
            query = query.filter(Note.priority == Priority(priority))
        
        # Filter by categories if provided
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return (
            query
            .order_by(desc(Note.updated_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_todos(
        self, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_ids: Optional[List[int]] = None
    ) -> int:
        """Count todos with optional filtering"""
        query = (
            self.db.query(Note)
            .filter(Note.note_type == NoteType.TODO)
            .filter(Note.is_archived == False)
        )
        
        # Filter by status if provided
        if status:
            query = query.filter(Note.todo_status == TodoStatus(status))
        
        # Filter by priority if provided
        if priority:
            query = query.filter(Note.priority == Priority(priority))
        
        # Filter by categories if provided
        if category_ids:
            query = (
                query
                .join(note_categories)
                .filter(note_categories.c.category_id.in_(category_ids))
                .distinct()
            )
        
        return query.count()