from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..services.note_service import NoteService
from ..schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from ..utils.exceptions import NotesAppException, to_http_exception

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.create_note(note_data)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/active", response_model=NoteListResponse)
def get_active_notes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category_ids: Optional[List[int]] = Query(None, description="Filter by category IDs"),
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        result = service.get_active_notes(
            page=page,
            page_size=page_size,
            category_ids=category_ids
        )
        return result
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/archived", response_model=NoteListResponse)
def get_archived_notes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category_ids: Optional[List[int]] = Query(None, description="Filter by category IDs"),
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        result = service.get_archived_notes(
            page=page,
            page_size=page_size,
            category_ids=category_ids
        )
        return result
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.get_note(note_id)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.update_note(note_id, note_data)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        service.delete_note(note_id)
    except NotesAppException as e:
        raise to_http_exception(e)


@router.patch("/{note_id}/archive", response_model=NoteResponse)
def archive_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.archive_note(note_id)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.patch("/{note_id}/unarchive", response_model=NoteResponse)
def unarchive_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.unarchive_note(note_id)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/todos", response_model=NoteListResponse)
def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by todo status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    category_ids: Optional[List[int]] = Query(None, description="Filter by category IDs"),
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        result = service.get_todos(
            page=page,
            page_size=page_size,
            status=status,
            priority=priority,
            category_ids=category_ids
        )
        return result
    except NotesAppException as e:
        raise to_http_exception(e)


@router.patch("/{note_id}/status", response_model=NoteResponse)
def update_todo_status(
    note_id: int,
    status: str = Query(..., description="New todo status"),
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        note = service.update_todo_status(note_id, status)
        return note
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/search/{search_term}", response_model=List[NoteResponse])
def search_notes(
    search_term: str,
    include_archived: bool = Query(False, description="Include archived notes in search"),
    category_ids: Optional[List[int]] = Query(None, description="Filter by category IDs"),
    db: Session = Depends(get_db)
):
    try:
        service = NoteService(db)
        notes = service.search_notes(
            search_term=search_term,
            include_archived=include_archived,
            category_ids=category_ids
        )
        return notes
    except NotesAppException as e:
        raise to_http_exception(e)