import json
import configparser

from typing import Optional
from fastapi import Depends, status, Security, Request, Response
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi_cache import FastAPICache

from exceptions.execption import AuthenticationError
from core.config import configs
from core.const import consts
from db.model.T_ACCOUNT import T_ACCOUNT as AC


import logging
logger = logging.getLogger(__name__)


def get_mysqlDb(request: Request):
    return request.state.mysqlDb


def get_message_object():
    msg_obj = configparser.ConfigParser()
    msg_obj.read(configs.MESSAGE_PATH, "UTF-8")
    msg_config = msg_obj["KOREAN"]

    return msg_config
