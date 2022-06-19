# pylint: disable=E0611, W0622
from datetime import date
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.json import ENCODERS_BY_TYPE
from sqlalchemy.orm import Session

from shifts.app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    **Parameters**
    * `model`: A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Select a single record by ID
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Select multiple records without a filter with the ptional parameters skip and limit
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record and insert it into the table
        """
        # Override the default jsonable_encoder behaviour
        ENCODERS_BY_TYPE[date] = lambda date_obj: date_obj

        obj_in_data = jsonable_encoder(obj_in)

        # Revert the override
        ENCODERS_BY_TYPE[date] = date.isoformat
        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete the specified record by ID
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
