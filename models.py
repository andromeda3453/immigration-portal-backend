from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class UserDetails(BaseModel):
    full_name: Optional[str]
    primary_email: Optional[EmailStr]
    alternative_email: Optional[EmailStr]
    contact_number: Optional[str]
    alternative_contact: Optional[str]

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str
