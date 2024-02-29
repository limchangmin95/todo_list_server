from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Float, String, Numeric, Date, Integer, SmallInteger

Base = declarative_base()

class T_TODO_CATEGORY(Base):
    __tablename__ = 'T_TODO_CATEGORY'

    td_category_seq = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    td_category_nm = Column(String(100), nullable=False)
    td_user_id = Column(String(30), nullable=False)
    sys_create_id = Column(String(30), nullable=False)
    sys_create_dt = Column(Date, nullable=False)
    sys_update_id = Column(String(30), nullable=False)
    sys_update_dt = Column(Date, nullable=False)