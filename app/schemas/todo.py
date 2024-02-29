from types import NoneType
from pydantic import BaseModel, validator, Field
from datetime import date
import logging

logger = logging.getLogger(__name__)

class ComboBase(BaseModel):
    label: str = None
    code: str = None

    class Config:
        orm_mode = True   

class ComboList(BaseModel):
    data: list[ComboBase] = []
    class Config:
        orm_mode = True  
class SearchTodoParam(BaseModel):
    id: str
    td_category_seq: int
    class Config:
        orm_mode = True

class TodoInfo(BaseModel):
    td_seq: int = None
    td_title: str = None
    td_detail: str = None
    td_favorite: str = None
    td_time: float = None
    td_main_seq: str = None
    create_dt: str

    @validator("create_dt", pre=True)
    def parse_create_dt(cls, v: date):
        if v:
            return v.strftime("%Y-%m-%d")
        else:
            return ''
    class Config:
        orm_mode = True

class CategoryInfo(BaseModel):
    td_category_seq: int
    td_category_nm: str
    create_dt: str

    @validator("create_dt", pre=True)
    def parse_create_dt(cls, v: date):
        if v:
            return v.strftime("%Y-%m-%d")
        else:
            return ''

    class Config:
        orm_mode = True

class TodoList(BaseModel):
    todo_list: list[TodoInfo] = []
    category_list: list[CategoryInfo] = []

    class Config:
        orm_mode = True

class TodoRegisterParam(BaseModel):
    id: str
    wish_img_path : str
    wish_nm: str
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    wish_addr: str
    wish_addr_full: str
    wish_addr_sub: str
    wish_latitude: float
    wish_longitude: float

    class Config:
        orm_mode = True

class TodoRegisterCreate(BaseModel):
    acc_seq: int
    wish_img_path : str
    wish_nm: str
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    wish_addr: str
    wish_addr_sub: str
    wish_addr_full: str
    wish_latitude: float
    wish_longitude: float

    class Config:
        orm_mode = True

class TodoUpdateParam(BaseModel):
    id: str
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    class Config:
        orm_mode = True

class TodoUpdateCreate(BaseModel):
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    class Config:
        orm_mode = True

class TodoMes(BaseModel):
    message: str

    class Config:
        orm_mode = True