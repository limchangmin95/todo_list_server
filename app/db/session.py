from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import configs

mysql_engine = create_engine(configs.MYSQL_DATABASE_URI, pool_pre_ping=True, pool_size=15)
MysqlSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=mysql_engine)