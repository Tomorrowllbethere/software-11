# схеми. валідація вхідних і вихідних  даних
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, constr
import re

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name:str = Field(max_length=50)
    email: EmailStr
    phone_number:str = Field(pattern=r'^\+?1?\d{9,15}$')
    date_of_birth: date
    


class ContactModel(ContactBase):
    info: Optional[constr(max_length=350)]
    


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True
