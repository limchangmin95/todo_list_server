from fastapi import APIRouter

from api.api_v1 import account, todo


api_router = APIRouter()

api_router.include_router(todo.router, prefix="/todo")
api_router.include_router(account.router, prefix="/user")
