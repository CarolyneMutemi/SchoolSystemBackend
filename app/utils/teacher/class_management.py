from fastapi import HTTPException

from app.utils.db.students import add_student, edit_student, delete_student
from app.utils.db.students import get_student_by_id
from app.utils.db.school_config import find_stream_by_name, find_form_by_level
from app.utils.db.school_config import find_subject_by_code, find_all_subjects
from app.utils.db.counter import get_next_admission_number
from app.utils.shared.auth import hash_password
from app.schemas.student.profile import Student
from app.schemas.teacher.auth import Class


def class_exists(form: int, stream: str) -> bool:
    """
    Check if a class exists.
    """
    found_stream = find_stream_by_name(stream)
    found_form = find_form_by_level(form)
    if not found_stream or not found_form:
        raise HTTPException(status_code=400, detail=f"Class {form} stream {stream} does not exist.")
    return True

def all_subject_codes():
    subjects = find_all_subjects()
    subject_codes = [subject.get("code") for subject in subjects]
    return subject_codes

def subject_exists(subject_code: str) -> bool:
    """
    Check if a subject exists.
    """
    subject = find_subject_by_code(subject_code)
    if not subject:
        raise HTTPException(status_code=400, detail="Subject does not exist.")
    return True

def is_the_class_teacher(class_obj: Class, current_teacher: dict) -> bool:
    class_exists(class_obj.form, class_obj.stream)
    classes_in_charge = current_teacher.get("classes_in_charge")
    
    print("Classes in charge: ", classes_in_charge)
    for class_in_charge in classes_in_charge:
        print("Class in charge: ", class_in_charge)
        print(f"Type of class_in_charge.form: {type(class_in_charge.get("form"))}, type of class_obj.form: {type(class_obj.form)}")
        if class_in_charge.get("form") == class_obj.form and class_in_charge.get("stream").lower() == class_obj.stream.lower():
            print("Teacher is in charge of the class.")
            return True
    raise HTTPException(status_code=400, detail="Teacher is not in charge of the class.")
    

def register_student(student: Student, current_teacher: dict):
    """
    Register a student.
    """
    # Check if the teacher is in charge of the class
    class_obj = Class(stream=student.stream, form=student.form)
    is_the_class_teacher(class_obj, current_teacher)
    student = student.model_dump()
    student["admission_number"] = str(get_next_admission_number())
    student["password"] = hash_password(student["password"])
    student = add_student(student)
    return student

def edit_a_student(student_id: str, student: Student):
    """
    Edit a student.
    """
    form = student.form
    stream = student.stream
    class_exists(form, stream)
    student = student.model_dump()
    student = edit_student(student_id, student)
    return student

def delete_a_student(student_id: str, current_teacher: dict):
    """
    Delete a student.
    """
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=400, detail="Student does not exist.")
    
    student_obj = Student(**student)
    class_obj = Class(stream=student_obj.stream, form=student_obj.form)
    is_the_class_teacher(class_obj, current_teacher)
    delete_student(student_id)
