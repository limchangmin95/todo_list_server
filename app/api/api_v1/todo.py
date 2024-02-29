from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, between, or_, and_, case, text
from db.crud.base import CRUDBase
from db.model.T_TODO import T_TODO as TD
from db.model.T_TODO_CATEGORY import T_TODO_CATEGORY as TD_CA
from api import deps
from schemas import todo

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/todo_list")
async def search_todo_list(
    search_form: todo.SearchTodoParam,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logger.debug("search_todo_list START!!!")
    logger.debug(search_form)

    category_sql = mysqlDb.query(
        TD_CA.td_category_seq,
        TD_CA.td_category_nm,
        TD_CA.sys_create_dt.label('create_dt'),
    )

    category_sql = category_sql.filter(TD_CA.td_user_id == search_form.td_category_seq)

    category_sql = category_sql.order_by(TD_CA.sys_update_dt.desc())

    category_list = category_sql.all()

    todo_sql = await get_todo_list(db=mysqlDb)

    todo_sql = todo_sql.filter(TD.sys_create_id == search_form.id)

    todo_sql = todo_sql.filter(TD.td_category_seq == search_form.td_category_seq)

    todo_sql = todo_sql.order_by(TD.sys_create_dt.desc())

    todo_list = todo_sql.all()

    return todo.TodoList(todo_list=todo_list, category_list=category_list)


# @router.post("/register")
# async def register_wish(
#     form_param: todo.WishRegisterParam,
#     mysqlDb: Session = Depends(deps.get_mysqlDb)
# ):
#     logging.debug("register_wish START!!!")
#     logging.debug(form_param)

#     obj_in = todo.WishRegisterCreate(
#         acc_seq=1,
#         wish_addr=form_param.wish_addr,
#         wish_addr_full=form_param.wish_addr_full,
#         wish_addr_sub=form_param.wish_addr_sub,
#         wish_img_path=form_param.wish_img_path,
#         wish_nm=form_param.wish_nm,
#         wish_rating=form_param.wish_rating,
#         wish_latitude=form_param.wish_latitude,
#         wish_longitude=form_param.wish_longitude,
#         wish_type=form_param.wish_type,
#         wish_sub_type=form_param.wish_sub_type,
#     )
    
#     CRUDBase.create(self=CRUDBase(TD), db=mysqlDb, obj_in=obj_in, login_id=form_param.id)

#     sql = await get_wish_list(db=mysqlDb)

#     sql = sql.filter(TD.sys_create_id == form_param.id)

#     wish_list = sql.all()

#     return todo.WishList(data=wish_list)


# @router.put("/update/{wish_seq}")
# async def update_wish(
#     wish_seq: int,
#     form_param: todo.WishUpdateParam,
#     mysqlDb: Session = Depends(deps.get_mysqlDb)
# ):
#     logger.debug('update_wish START!!!!')
#     logger.debug(wish_seq)
#     logger.debug(form_param)

#     db_obj = mysqlDb.query(TD).filter(TD.wish_seq == wish_seq).first()

#     obj_wish_in = todo.WishUpdateCreate(
#         wish_type=form_param.wish_type,
#         wish_sub_type=form_param.wish_sub_type,
#         wish_rating=form_param.wish_rating,
#     )
    
#     CRUDBase.update(self=CRUDBase(TD), db=mysqlDb, db_obj=db_obj, obj_in=obj_wish_in, login_id='test')

#     sql = await get_wish_list(db=mysqlDb)

#     sql = sql.filter(TD.sys_create_id == form_param.id)

#     wish_list = sql.all()

#     return todo.WishList(data=wish_list)


# @router.delete("/delete/{wish_seq}/{id}")
# async def delete_wish(
#     wish_seq: int,
#     id: str,
#     mysqlDb: Session = Depends(deps.get_mysqlDb)
# ):
#     logger.debug('delete_wish START!!!!')
#     logger.debug(wish_seq)
    
#     CRUDBase.remove(self=CRUDBase(TD), db=mysqlDb, id=wish_seq)

#     sql = await get_wish_list(db=mysqlDb)

#     sql = sql.filter(TD.sys_create_id == id)

#     wish_list = sql.all()

#     return todo.WishList(data=wish_list)

    
async def get_todo_list(
    db: Session,
):
    logger.debug('get_todo_list START!!!!!')

    sql = db.query(
        TD.td_seq,
        TD.td_success_flg,
        TD.td_title,
        TD.td_detail,
        TD.td_favorite,
        TD.td_time,
        TD.td_main_seq,
        TD.sys_create_dt.label("create_dt"),
    )

    return sql