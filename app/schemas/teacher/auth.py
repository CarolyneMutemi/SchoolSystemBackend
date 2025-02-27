from pydantic import BaseModel, EmailStr
from typing import List, Optional


class class_taught(BaseModel):
    form: int
    stream: str
    subject: str

class Class(BaseModel):
    form: int
    stream: str

class Teacher(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    national_id: str
    enrollment_date: str
    qualified_subjects: List[str]
    classes_taught: List[class_taught]
    classes_in_charge: List[Class]

class LoginData(BaseModel):
    email: EmailStr
    password: str

class Class(BaseModel):
    form: int
    stream: str 
