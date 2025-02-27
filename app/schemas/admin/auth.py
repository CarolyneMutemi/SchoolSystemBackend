from pydantic import BaseModel, EmailStr


class Admin(BaseModel):
    nationalID: str
    phone_number: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    enrollment_date: str


class NewPassword(BaseModel):
    current_password: str
    new_password: str
