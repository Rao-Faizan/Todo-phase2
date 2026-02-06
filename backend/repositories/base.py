from typing import TypeVar, Generic, Optional, List
from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar
from uuid import UUID

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model
        self.session = session

    def get(self, id: UUID) -> Optional[T]:
        """Get a record by ID"""
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()

    def get_all(self, offset: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        statement = select(self.model).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def create(self, obj: T) -> T:
        """Create a new record"""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, id: UUID, obj_update: T) -> Optional[T]:
        """Update a record by ID"""
        obj = self.get(id)
        if obj:
            for key, value in obj_update.dict(exclude_unset=True).items():
                setattr(obj, key, value)
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
        return obj

    def delete(self, id: UUID) -> bool:
        """Delete a record by ID"""
        obj = self.get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False