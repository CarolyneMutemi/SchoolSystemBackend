from pydantic import BaseModel, EmailStr


class NewAdmin(BaseModel):
    nationalID: str
    phone_number: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    enrollment_date: str
