from typing import Optional
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy_utils import EmailType
# , PhoneNumberType


from src.database.db import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    # phone: Optional[PhoneNumberType] = Field(None)
    phone = Column(String(20))
    birthday = Column(Date)
    # Optional[Date] = None
    info = Column(String(200))
    created_at = Column('created_at', DateTime, default=func.now())
    