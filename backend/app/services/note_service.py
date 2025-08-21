from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from ..repositories.note_repository import NoteRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.note import NoteCreate, NoteUpdate, NoteListResponse
from ..models.note import Note
from ..utils.exceptions import NotFoundError, ValidationError
import math


class NoteService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repository = NoteRepository(db)
        self.category_repository = CategoryRepository(db)
    
    def create_note(self, note_data: NoteCreate) -> Note:
        # Validate categories exist
        if note_data.category_ids:
            categories = self.category_repository.get_categories_by_ids(note_data.category_ids)
            if len(categories) != len(note_data.category_ids):
                raise ValidationError("One or more category IDs are invalid")
        
        # Create note
        note_dict = note_data.model_dump(exclude={'category_ids'})
        note = self.note_repository.create(note_dict)
        
        # Add categories to note
        if note_data.category_ids:
            categories = self.category_repository.get_categories_by_ids(note_data.category_ids)
            note.categories = categories
            self.db.commit()
            self.db.refresh(note)
        
        return self.note_repository.get_by_id_with_categories(note.id)
    
    def get_note(self, note_id: int) -> Note:
        note = self.note_repository.get_by_id_with_categories(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        return note
    
    def get_active_notes(
        self, 
        page: int = 1, 
        page_size: int = 10,
        category_ids: Optional[List[int]] = None
    ) -> NoteListResponse:
        skip = (page - 1) * page_size
        
        notes = self.note_repository.get_active_notes(
            skip=skip, 
            limit=page_size,
            category_ids=category_ids
        )
        
        total = self.note_repository.count_active_notes(category_ids)
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        return NoteListResponse(
            notes=notes,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def get_archived_notes(
        self, 
        page: int = 1, 
        page_size: int = 10,
        category_ids: Optional[List[int]] = None
    ) -> NoteListResponse:
        skip = (page - 1) * page_size
        
        notes = self.note_repository.get_archived_notes(
            skip=skip, 
            limit=page_size,
            category_ids=category_ids
        )
        
        total = self.note_repository.count_archived_notes(category_ids)
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        return NoteListResponse(
            notes=notes,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def update_note(self, note_id: int, note_data: NoteUpdate) -> Note:
        note = self.note_repository.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        
        # Validate categories if provided
        if note_data.category_ids is not None:
            if note_data.category_ids:
                categories = self.category_repository.get_categories_by_ids(note_data.category_ids)
                if len(categories) != len(note_data.category_ids):
                    raise ValidationError("One or more category IDs are invalid")
        
        # Update basic fields
        update_dict = note_data.model_dump(exclude={'category_ids'}, exclude_unset=True)
        if update_dict:
            self.note_repository.update(note_id, update_dict)
        
        # Update categories if provided
        if note_data.category_ids is not None:
            note = self.note_repository.get_by_id_with_categories(note_id)
            if note_data.category_ids:
                categories = self.category_repository.get_categories_by_ids(note_data.category_ids)
                note.categories = categories
            else:
                note.categories = []
            self.db.commit()
            self.db.refresh(note)
        
        return self.note_repository.get_by_id_with_categories(note_id)
    
    def delete_note(self, note_id: int) -> bool:
        note = self.note_repository.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        
        return self.note_repository.delete(note_id)
    
    def archive_note(self, note_id: int) -> Note:
        note = self.note_repository.archive_note(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        return self.note_repository.get_by_id_with_categories(note_id)
    
    def unarchive_note(self, note_id: int) -> Note:
        note = self.note_repository.unarchive_note(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        return self.note_repository.get_by_id_with_categories(note_id)
    
    def get_todos(
        self, 
        page: int = 1, 
        page_size: int = 10,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_ids: Optional[List[int]] = None
    ) -> NoteListResponse:
        skip = (page - 1) * page_size
        
        notes = self.note_repository.get_todos(
            skip=skip, 
            limit=page_size,
            status=status,
            priority=priority,
            category_ids=category_ids
        )
        
        total = self.note_repository.count_todos(status, priority, category_ids)
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        return NoteListResponse(
            notes=notes,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    def update_todo_status(self, note_id: int, status: str) -> Note:
        note = self.note_repository.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note", note_id)
        
        if note.note_type.value != "todo":
            raise ValidationError("Note is not a todo item")
        
        # Validate status
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            raise ValidationError(f"Invalid status. Must be one of: {valid_statuses}")
        
        self.note_repository.update(note_id, {"todo_status": status})
        return self.note_repository.get_by_id_with_categories(note_id)
    
    def search_notes(
        self, 
        search_term: str, 
        include_archived: bool = False,
        category_ids: Optional[List[int]] = None
    ) -> List[Note]:
        return self.note_repository.search_notes(
            search_term=search_term,
            include_archived=include_archived,
            category_ids=category_ids
        )