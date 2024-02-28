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

@router.get("/me")
def login(
    mysqlDb: Session = Depends(deps.get_mysqlDb)
):
    logger.debug('login START!!!!!')