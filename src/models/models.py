from typing import Optional
from sqlalchemy import Column, Integer, String, func, extract
from sqlalchemy.orm import column_property
from sqlalchemy.sql.sqltypes import Date, DateTime
from datetime import datetime
from sqlalchemy_utils import EmailType
from sqlalchemy.ext.hybrid import hybrid_property
# PhoneNumberType


from src.database.db import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    phone = Column(String(12))
    birthday = Column(Date)
    info = Column(String(200))
    created_at = Column('created_at', DateTime, default=func.now())
    b_date = column_property(func.to_date(func.concat(datetime.today().year, '-', extract('month', birthday), '-', extract('day', birthday)), 'YYYY-MM-DD'))
    