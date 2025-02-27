from fastapi import HTTPException, status
from bson import ObjectId

from app.db.mongo_db import students_collection


def get_students_in_a_class(form: int, stream: str):
    """
    Get all students in a class.
    """
    cursor = students_collection.find({"form": form, "stream": stream.lower()})
    students = list(cursor)

    for student in students:
        student["_id"] = str(student["_id"])
        del student["password"]
    return students

def get_student_by_admission_number(admission_number: int):
    """
    Get student by admission number.
    """
    student = students_collection.find_one({"admission_number": admission_number})
    if student:
        student["_id"] = str(student["_id"])
    print("Student is: ", student)
    return student

def get_student_by_id(student_id: str):
    """
    Get student by id.
    """
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        student["_id"] = str(student["_id"])
        del student["password"]
    return student

def add_student(student: dict):
    """
    Add a student.
    """
    student_is_added = get_student_by_admission_number(student["admission_number"])
    if student_is_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with similar admission number already exists.")
    result = students_collection.insert_one(student)
    student["_id"] = str(result.inserted_id)
    return student

def edit_student(student_id: str, student: dict):
    """
    Edit student.
    """
    student_is_added = get_student_by_id(student_id)
    if not student_is_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student does not exist.")
    students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": student})
    student["_id"] = student_id
    return student

def delete_student(student_id: str):
    """
    Delete student by id.
    """
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist.")
    return True
