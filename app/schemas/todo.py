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

class ComboTypeBase(ComboBase):
    type: str = None
    class Config:
        orm_mode = True   
class ComboList(BaseModel):
    data: list[ComboBase] = []
    class Config:
        orm_mode = True  

class ComboTypeList(BaseModel):
    data: list[ComboTypeBase] = []
    class Config:
        orm_mode = True 
class SearchWishParam(BaseModel):
    id: str
    searchKeyword: str = None
    searchType: str = None
    searchType2: str = None
    searchAddr: str = None
    searchAddrSub: str = None
    
    class Config:
        orm_mode = True

class WishInfo(BaseModel):
    wish_seq: int
    wish_nm: str
    wish_addr: str
    wish_addr_full: str
    wish_rating: float = None
    wish_img_path: str = None
    wish_latitude: float
    wish_longitude: float
    wish_type: str
    wish_type_nm: str
    wish_sub_type: str
    wish_sub_type_nm: str
    create_dt: str

    @validator("create_dt", pre=True)
    def parse_create_dt(cls, v: date):
        if v:
            return v.strftime("%Y-%m-%d")
        else:
            return ''
        
    @validator("wish_sub_type", pre=True)
    def parse_sub_type(cls, v: date):
        if v is None:
            return '0'
        else:
            return v     
    @validator("wish_sub_type_nm", pre=True)
    def parse_sub_type_nm(cls, v: date):
        if v is None:
            return '미선택'
        else:
            return v

    class Config:
        orm_mode = True

class WishList(BaseModel):
    data: list[WishInfo] = []

    class Config:
        orm_mode = True

class WishRegisterParam(BaseModel):
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


class WishRegisterCreate(BaseModel):
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

class WishUpdateParam(BaseModel):
    id: str
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    class Config:
        orm_mode = True

class WishUpdateCreate(BaseModel):
    wish_rating: float = None
    wish_type: str
    wish_sub_type: str
    class Config:
        orm_mode = True

class WishMes(BaseModel):
    message: str

    class Config:
        orm_mode = True