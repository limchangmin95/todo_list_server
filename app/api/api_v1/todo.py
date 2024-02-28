from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, between, or_, and_, case, text
from db.crud.base import CRUDBase
from db.model.T_TODO import T_TODO as TD
from api import deps
from schemas import todo

import logging
logger = logging.getLogger(__name__)


router = APIRouter()



@router.post("/todo_list")
async def search_todo_list(
    search_form: todo.SearchWishParam,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logger.debug("get_wish_list START!!!")
    logger.debug(search_form)

    sql = await get_wish_list(db=mysqlDb)

    sql = sql.filter(TD.sys_create_id == search_form.id)

    if search_form.searchKeyword != "" and search_form.searchKeyword is not None:
        sql = sql.filter(TD.wish_nm.ilike(f"%{search_form.searchKeyword}%"))

    if search_form.searchType != "0" and search_form.searchType is not None:
        sql = sql.filter(TD.wish_type == search_form.searchType)

    if search_form.searchType2 != "0" and search_form.searchType2 is not None:
        sql = sql.filter(TD.wish_sub_type == search_form.searchType2)

    if search_form.searchAddr != "0" and search_form.searchAddr is not None:
        sql = sql.filter(TD.wish_addr == search_form.searchAddr)
    
    if search_form.searchAddrSub != "0" and search_form.searchAddrSub is not None:
        sql = sql.filter(TD.wish_addr_sub == search_form.searchAddrSub)

    sql = sql.order_by(TD.sys_create_dt.desc())

    wish_list = sql.all()

    return todo.WishList(data = wish_list)


@router.post("/register")
async def register_wish(
    form_param: todo.WishRegisterParam,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logging.debug("register_wish START!!!")
    logging.debug(form_param)

    obj_in = todo.WishRegisterCreate(
        acc_seq=1,
        wish_addr=form_param.wish_addr,
        wish_addr_full=form_param.wish_addr_full,
        wish_addr_sub=form_param.wish_addr_sub,
        wish_img_path=form_param.wish_img_path,
        wish_nm=form_param.wish_nm,
        wish_rating=form_param.wish_rating,
        wish_latitude=form_param.wish_latitude,
        wish_longitude=form_param.wish_longitude,
        wish_type=form_param.wish_type,
        wish_sub_type=form_param.wish_sub_type,
    )
    
    CRUDBase.create(self=CRUDBase(TD), db=mysqlDb, obj_in=obj_in, login_id=form_param.id)

    sql = await get_wish_list(db=mysqlDb)

    sql = sql.filter(TD.sys_create_id == form_param.id)

    wish_list = sql.all()

    return todo.WishList(data=wish_list)


@router.put("/update/{wish_seq}")
async def update_wish(
    wish_seq: int,
    form_param: todo.WishUpdateParam,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logger.debug('update_wish START!!!!')
    logger.debug(wish_seq)
    logger.debug(form_param)

    db_obj = mysqlDb.query(TD).filter(TD.wish_seq == wish_seq).first()

    obj_wish_in = todo.WishUpdateCreate(
        wish_type=form_param.wish_type,
        wish_sub_type=form_param.wish_sub_type,
        wish_rating=form_param.wish_rating,
    )
    
    CRUDBase.update(self=CRUDBase(TD), db=mysqlDb, db_obj=db_obj, obj_in=obj_wish_in, login_id='test')

    sql = await get_wish_list(db=mysqlDb)

    sql = sql.filter(TD.sys_create_id == form_param.id)

    wish_list = sql.all()

    return todo.WishList(data=wish_list)


@router.delete("/delete/{wish_seq}/{id}")
async def delete_wish(
    wish_seq: int,
    id: str,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logger.debug('delete_wish START!!!!')
    logger.debug(wish_seq)
    
    CRUDBase.remove(self=CRUDBase(TD), db=mysqlDb, id=wish_seq)

    sql = await get_wish_list(db=mysqlDb)

    sql = sql.filter(TD.sys_create_id == id)

    wish_list = sql.all()

    return todo.WishList(data=wish_list)

    
async def get_wish_list(
    db: Session,
):
    logger.debug('get_wish_list START!!!!!')

    sql = db.query(
        TD.wish_seq,
        TD.wish_nm,
        func.concat(TD.wish_addr + " " + TD.wish_addr_sub).label("wish_addr"),
        case((TD.wish_addr_full == None, ""), else_ = TD.wish_addr_full).label('wish_addr_full'),
        case(
            (TD.wish_type == "restaurant", "식당"),
            (TD.wish_type == "cafe", "카페"),
            (TD.wish_type == "convenience", "편의점"),
            (TD.wish_type == "super", "슈퍼"),
            (TD.wish_type == "accommodation", "숙소"),
            else_="주차장"
        ).label("wish_type_nm"),
        TD.wish_type,
        # func.coalesce(mysqlDb.query(TYPE.type_nm).filter(and_(TYPE.type_main == search_form.searchType, TYPE.type_sub == search_form.searchType2)), '미선택').label("wish_sub_type"),
        TD.wish_rating,
        TD.wish_latitude,
        TD.wish_longitude,
        TD.wish_img_path,
        TD.sys_create_dt.label("create_dt"),
        # func.count(TD.wish_seq).label(''),
    )

    return sql