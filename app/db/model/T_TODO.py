from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Float, String, Numeric, Date, Integer, SmallInteger

Base = declarative_base()

class T_TODO(Base):
    __tablename__ = 'T_TODO'

    td_seq = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    td_category_seq = Column(Integer, nullable=False)
    td_main_seq = Column(Integer)
    td_title = Column(String(100), nullable=False)
    td_detail = Column(String(1000))
    td_time = Column(Date)
    td_favorite = Column(String(1), nullable=False)
    td_success_flg = Column(String(1), nullable=False)
    sys_create_id = Column(String(30), nullable=False)
    sys_create_dt = Column(Date, nullable=False)
    sys_update_id = Column(String(30), nullable=False)
    sys_update_dt = Column(Date, nullable=False)