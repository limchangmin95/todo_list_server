from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.config import configs
from api import deps
from core.const import consts

import logging
logger = logging.getLogger(__name__)

origins = ["*"]
if configs.BACKEND_CORS_ORIGINS:
    origins = configs.BACKEND_CORS_ORIGINS

class Response():
    
    def authentication_error(req, msg):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content = Response.serialize_error(req, message.get(consts.E00002) if not msg else msg)
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def validate_error(req, msg):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = Response.serialize_error(req, message.get(consts.E00003) if not msg else msg)
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def record_not_found(req, msg):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = Response.serialize_error(req, message.get(consts.E00004) if not msg else msg)
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def file_error(req, msg):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = Response.serialize_error(req, message.get(consts.E00006) if not msg else message.get(msg))
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def sql_error(req, msg):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = Response.serialize_error(req, message.get(consts.E00003) if not msg else message.get(msg))
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def reqest_param_error(req, e):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            content = Response.serialize_error(req, message.get(consts.E00005))
        )
        Response.set_res_header_origin(res, req)
        return res
    
    def internal_server_error(req, e):
        message = deps.get_message_object()
        res = JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = Response.serialize_error(req, message.get(consts.E00006) if not str(e) else e)
        )
        Response.set_res_header_origin(res, req)

        return res

    @staticmethod
    def serialize_error(req, messages):
        message = deps.get_message_object()
        if not messages:
            return { "message" : message.get(consts.E00001) }
        else:
            if type(messages) is str:
                return { "message": messages }
            else:
                return { "message": str(messages) }
    
    @staticmethod
    def set_res_header_origin(res, req):
        origin = req.headers.get("origin")

        if origin in origins:
            res.headers["Access-Control-Allow-Origin"] = origin