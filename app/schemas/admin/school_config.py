from pydantic import BaseModel


class Grade(BaseModel):
    letter: str
    max_score: int
    min_score: int

class GradeResponse(Grade):
    _id: str

class Subject(BaseModel):
    name: str
    code: str

class SubjectResponse(Subject):
    _id: str

class Form(BaseModel):
    level: int

class FormResponse(Form):
    _id: str

class Stream(BaseModel):
    name: str

class StreamResponse(Stream):
    _id: str
