from typing import Any, Optional
from pydantic import AnyHttpUrl, BaseSettings, validator

class Configs(BaseSettings):

    ## BASE
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    # ENCRYPT_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # 60 minutes * 12 hours
    # SECRET_KEY: str
    # HASH_SALT: str
    SERVER_PORT: int
    SERVER_TYPE: str

    # SERVER_HOST_AWS: str
    SERVER_HOST_LOCAL: str
    SERVER_HOST: str = None

    MESSAGE_PATH: str
    
    @validator("SERVER_HOST", pre=True)
    def assemble_server_host(cls, v: str, values: dict[str, Any]) -> str:
        if not v:
            if values.get("SERVER_TYPE") == "LOCAL":
                return values.get("SERVER_HOST_LOCAL")
            else:
                return values.get("SERVER_HOST_AWS")
        return v
    
    BACKEND_CORS_ORIGINS_URL: str
    BACKEND_CORS_ORIGINS: list = None
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: list, values: dict[str, Any]) -> list:
        if not v:
            urls = values.get("BACKEND_CORS_ORIGINS_URL")
            if urls:
                return urls.split(",")
        return v

    LOG_INI_PATH: str

    ## redis
    REDIS_URL: str

    ## AWS S3
    # S3_BUCKET: str
    # S3_REGION: str
    # S3_ACCESS_KEY_ID: str
    # S3_SECRET_ACCESS_KEY: str

    ## DB_MYSQL
    # MYSQL_SERVER_AWS:str
    MYSQL_SERVER_LOCAL:str
    MYSQL_SERVER: str = None

    @validator("MYSQL_SERVER", pre=True)
    def assemble_mysql_server(cls, v: str, values: dict[str, Any]) -> str:
        if not v:
            if values.get("SERVER_TYPE") == "LOCAL":
                return values.get("MYSQL_SERVER_LOCAL")
            else:
                return values.get("MYSQL_SERVER_AWS")
        return v

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_DATABASE_URI: Optional[str] = None

    @validator("MYSQL_DATABASE_URI", pre=True)
    def assemble_mysql_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if not v:
            return 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
                      'user': values.get("MYSQL_USER"),
                      'password': values.get("MYSQL_PASSWORD"),
                      'host': values.get("MYSQL_SERVER"),
                      'dbname': values.get("MYSQL_DB")
                  })
        return v

    class Config:
        env_file = '../.env'
        case_sensitive = True


configs = Configs()