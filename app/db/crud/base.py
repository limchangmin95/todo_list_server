import logging

from typing import Any, Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

ModelType = TypeVar("ModelType", bound=declarative_base())
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    #def get(self, db: Session, id: Any) -> Optional[ModelType]:
    #    return db.query(self.model).filter(self.model.id == id).first()


    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, login_id: str, is_commit: bool = True) -> ModelType:
        now = datetime.now()
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data.update({
            "sys_create_id": login_id,
            "sys_create_dt": now,
            "sys_update_id": login_id,
            "sys_update_dt": now
        })

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        # if is_commit:
        #     db.commit()
        #     db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        login_id: str,
    ) -> ModelType:


        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data.update({"sys_update_id": login_id, "sys_update_dt": datetime.now()})

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        
        # if (is_commit):
        #     db.commit()
        #     db.refresh(db_obj)

        return db_obj
    def remove(self, db: Session, *, id: int, is_commit = False) -> ModelType:
       obj = db.query(self.model).get(id)
       db.delete(obj)
       # if is_commit:
       #     db.commit()
       return obj
    
    # todo delete時のロックバージョン確認
    # def remove(self, db: Session, *, id: int, is_commit = False, is_version_check: bool = True) -> ModelType:
    #     obj = db.query(self.model).get(id)
    #     if is_version_check:
    #         if type(obj) is dict:
    #             if "lock_version" not in obj or obj["lock_version"] is None:
    #                 raise SqlError(consts.E00010)
    #         elif obj.lock_version != obj["lock_version"]:
    #             raise SqlError(consts.E00011)
    #     else:
    #         if not hasattr(obj, 'lock_version') or obj.lock_version is None:
    #             raise SqlError(consts.E00010)
    #         elif obj.lock_version != obj.lock_version:
    #             raise SqlError(consts.E00011)

    #     db.delete(obj)
    #     # if is_commit:
    #     #     db.commit()
    #     return obj
    
    def bulk_create(self, db: Session, *, obj_list_in: list[CreateSchemaType], login_id: str, is_commit: bool = True) -> ModelType:
        now = datetime.now()
        target_data = []
        
        for obj_in in obj_list_in:
            obj_in_data = jsonable_encoder(obj_in)
            obj_in_data.update({
                "sys_create_id": login_id,
                "sys_create_dt": now,
                "sys_update_id": login_id,
                "sys_update_dt": now
            })

            target_data.append(obj_in_data)

        db.execute(self.model.__table__.insert(), target_data)
        # if is_commit:
        #     db.commit()
        #     db.refresh()
        return
    

