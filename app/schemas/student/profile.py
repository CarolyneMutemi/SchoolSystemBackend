from pydantic import BaseModel
from typing import List, Optional


class Parent(BaseModel):
    relationship: str
    first_name: str
    last_name: str
    phone_number: str
    email: str
    Address: str

class StudentSchema(BaseModel):
    first_name: str
    last_name: str
    form: int
    stream: str
    date_of_birth: str
    enrollment_date: str
    phone_number: str
    email: str
    address: str
    parents: List[Parent]

class Student(StudentSchema):
    password: str

class StudentResponse(StudentSchema):
    _id: str
    admission_number: int
