from pydantic import BaseModel


class SubjectResult(BaseModel):
    student_adm_no: int
    student_name: str
    form: int
    stream: str
    year: int
    term: int
    subject: str
    marks: int
