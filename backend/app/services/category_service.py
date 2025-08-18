from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryCreate, CategoryUpdate
from ..models.category import Category
from ..utils.exceptions import NotFoundError, DuplicateError


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)
    
    def create_category(self, category_data: CategoryCreate) -> Category:
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category:
            raise DuplicateError("Category", "name", category_data.name)
        
        category_dict = category_data.model_dump()
        return self.repository.create(category_dict)
    
    def get_category(self, category_id: int) -> Category:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", category_id)
        return category
    
    def get_all_categories(self) -> List[Category]:
        return self.repository.get_all(order_by="name")
    
    def get_categories_with_count(self) -> List[dict]:
        categories_with_count = self.repository.get_with_notes_count()
        return [
            {
                "category": category,
                "notes_count": count
            }
            for category, count in categories_with_count
        ]
    
    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Category:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", category_id)
        
        # Check name uniqueness if name is being updated
        if category_data.name and category_data.name != category.name:
            existing_category = self.repository.get_by_name(category_data.name)
            if existing_category:
                raise DuplicateError("Category", "name", category_data.name)
        
        update_dict = category_data.model_dump(exclude_unset=True)
        updated_category = self.repository.update(category_id, update_dict)
        if not updated_category:
            raise NotFoundError("Category", category_id)
        
        return updated_category
    
    def delete_category(self, category_id: int) -> bool:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise NotFoundError("Category", category_id)
        
        return self.repository.delete(category_id)
    
    def search_categories(self, search_term: str) -> List[Category]:
        return self.repository.search_by_name(search_term)