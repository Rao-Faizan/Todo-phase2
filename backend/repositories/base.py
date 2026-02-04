"""Base repository class for common database operations"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from sqlmodel import Session
from uuid import UUID


T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    """Base repository class providing common database operations"""

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID"""
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass

    @abstractmethod
    def update(self, id: UUID, entity: T) -> Optional[T]:
        """Update an existing entity"""
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        """Delete an entity"""
        pass