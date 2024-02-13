from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    email: EmailStr = Field(max_length=80)
    birthday: Optional[date] = Field(None)
    phone:  Optional[str] = Field(max_length=20)
    info: Optional[str] = Field(max_length=200)
    

class ContactUpdateSchema(ContactSchema):
    created_at: datetime

class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    birthday: date
    phone: str
    info: str

    class Config:
        from_attributes = True