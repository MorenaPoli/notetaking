from fastapi import HTTPException
from typing import Any, Optional


class NotesAppException(Exception):
    """Base exception class for the notes app"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(NotesAppException):
    """Exception raised when a resource is not found"""
    def __init__(self, resource: str, resource_id: Any):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, 404)


class ValidationError(NotesAppException):
    """Exception raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class DuplicateError(NotesAppException):
    """Exception raised when trying to create a duplicate resource"""
    def __init__(self, resource: str, field: str, value: Any):
        message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message, 409)


def to_http_exception(exception: NotesAppException) -> HTTPException:
    """Convert custom exception to FastAPI HTTPException"""
    return HTTPException(
        status_code=exception.status_code,
        detail=exception.message
    )