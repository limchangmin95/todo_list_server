import uvicorn
import logging
import locale
import random
import string
import time
import os

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from core.config import configs
from fastapi.responses import JSONResponse
from exceptions.execption import RecordNotFoundError, ValidateError, AuthenticationError, FileError, SqlError
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from db.session import MysqlSessionLocal

from fastapi.exceptions import RequestValidationError
from api.api_v1.api import api_router
from api.response import Response as Res


logging.config.fileConfig(configs.LOG_INI_PATH, disable_existing_loggers=False)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')

app = FastAPI(
    title=configs.PROJECT_NAME, openapi_url=f"/openapi.json"
)

origins = ["*"]
if configs.BACKEND_CORS_ORIGINS:
    origins = configs.BACKEND_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-authentication-token"]
)

app.include_router(api_router, prefix=configs.API_V1_STR)

@app.on_event('startup')
async def on_startup() -> None:
    redis = aioredis.from_url(configs.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="foodtable-cache")

##
## Intercept
##
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"================ START  {request.method} {request.url.path}  rid={idem}")
    start_time = time.time()

    request.state.mysqlDb: Session = MysqlSessionLocal()

    try:
        response: Response = await call_next(request)
    except ValidateError as e:
        logger.error("ValidateError : message -> " + str(e.msg))
        response = Res.validate_error(request, e.msg)
        request.state.mysqlDb.rollback()
    except RecordNotFoundError as e:
        logger.error("RecordNotFoundError : message -> " + str(e.msg))        
        response = Res.record_not_found(request, e.msg)
        request.state.mysqlDb.rollback()
    except SqlError as e:
        logger.error("SqlError : message -> " + str(e.msg))
        response = Res.sql_error(request, e.msg)
        request.state.mysqlDb.rollback()
    except AuthenticationError as e:
        logger.error("AuthenticationError : message -> " + str(e.msg))        
        response = Res.authentication_error(request, e.msg)
        request.state.mysqlDb.rollback()
    except Exception as e:
        logger.error(e)
        response = Res.internal_server_error(request, e)
        request.state.mysqlDb.rollback()
    else:
        if response.status_code == status.HTTP_200_OK:
            request.state.mysqlDb.commit()
        else:
            request.state.mysqlDb.rollback()
    finally:
        request.state.mysqlDb.close()
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"================ COMPLETE  {request.method} {request.url.path}  {formatted_process_time}ms  status={response.status_code}  rid={idem}")
    return response


@app.exception_handler(RequestValidationError)
async def handler(req:Request, e:RequestValidationError):
    logger.error(e)
    return Res.reqest_param_error(req, e)


if __name__ == '__main__':
    uvicorn.run("main:app", host=configs.SERVER_HOST, port=configs.SERVER_PORT, reload=True, log_level="info")