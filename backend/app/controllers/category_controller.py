from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.category_service import CategoryService
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithNotesCount
from ..utils.exceptions import NotesAppException, to_http_exception

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    try:
        service = CategoryService(db)
        category = service.create_category(category_data)
        return category
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    try:
        service = CategoryService(db)
        categories = service.get_all_categories()
        return categories
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/with-count", response_model=List[CategoryWithNotesCount])
def get_categories_with_count(db: Session = Depends(get_db)):
    try:
        service = CategoryService(db)
        categories_data = service.get_categories_with_count()
        
        result = []
        for item in categories_data:
            category = item["category"]
            count = item["notes_count"]
            result.append(CategoryWithNotesCount(
                id=category.id,
                name=category.name,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                notes_count=count
            ))
        
        return result
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = CategoryService(db)
        category = service.get_category(category_id)
        return category
    except NotesAppException as e:
        raise to_http_exception(e)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    try:
        service = CategoryService(db)
        category = service.update_category(category_id, category_data)
        return category
    except NotesAppException as e:
        raise to_http_exception(e)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = CategoryService(db)
        service.delete_category(category_id)
    except NotesAppException as e:
        raise to_http_exception(e)


@router.get("/search/{search_term}", response_model=List[CategoryResponse])
def search_categories(
    search_term: str,
    db: Session = Depends(get_db)
):
    try:
        service = CategoryService(db)
        categories = service.search_categories(search_term)
        return categories
    except NotesAppException as e:
        raise to_http_exception(e)