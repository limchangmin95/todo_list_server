from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Float, String, Numeric, Date, Integer, SmallInteger

Base = declarative_base()

class T_ACCOUNT(Base):
    __tablename__ = 'T_ACCOUNT'

    acc_seq = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    acc_id = Column(String(30), nullable=False)
    acc_pw = Column(String(1000), nullable=False)
    acc_in_time = Column(Date)
    acc_out_time = Column(Date)
    sys_create_id = Column(String(30), nullable=False)
    sys_create_dt = Column(Date, nullable=False)
    sys_update_id = Column(String(30), nullable=False)
    sys_update_dt = Column(Date, nullable=False)
