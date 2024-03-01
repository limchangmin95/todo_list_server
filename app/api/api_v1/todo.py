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
    
    category_data = None
    todo_data = None

    category_sql = await get_category_list(db=mysqlDb)

    category_list = category_sql.all()

    category_data = todo.CategoryData(
        data=category_list
    )

    todo_list = []

    if len(category_list) != 0:
        td_category = category_list[0]
        
        logger.debug('td_category START!!!!')
        logger.debug(td_category.td_category_seq)

        todo_sql = await get_todo_list(db=mysqlDb)

        todo_sql = todo_sql.filter(TD.sys_create_id == search_form.id)

        todo_sql = todo_sql.filter(TD.td_category_seq == td_category.td_category_seq)

        todo_sql = todo_sql.order_by(TD.sys_create_dt.desc())

        todo_list = todo_sql.all()

        todo_data = todo.TodoData(
            data=todo_list
        )

    return todo.TodoList(category_list=category_data, todo_list=todo_data)


@router.post("/category/register")
async def register_category(
    form_param: todo.TodoCategoryParam,
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logging.debug("register_category START!!!")
    logging.debug(form_param)

    obj_in = todo.TodoCategoryCreate(
       td_category_nm=form_param.td_category_nm, 
       td_user_id=form_param.id
    )
    
    CRUDBase.create(self=CRUDBase(TD_CA), db=mysqlDb, obj_in=obj_in, login_id=form_param.id)

    sql = await get_category_list(db=mysqlDb)

    sql = sql.filter(TD_CA.sys_create_id == form_param.id)

    category_list = sql.all()

    logger.debug('register_category END')
    logger.debug(category_list)

    return todo.CategoryData(data=category_list)


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


async def get_category_list(
        db: Session,
):
    logger.debug('get_category_list START!!!!!')

    sql = db.query(
        TD_CA.td_category_seq,
        TD_CA.td_category_nm,
        TD_CA.sys_create_dt.label('create_dt'),
    )

    sql = sql.order_by(TD_CA.sys_create_dt.asc())

    return sql