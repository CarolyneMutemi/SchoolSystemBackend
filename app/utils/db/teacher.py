from fastapi import HTTPException
from bson import ObjectId

from app.db.mongo_db import teachers_collection


def find_teacher_by_email(email: str) -> dict:
    """
    Find teacher by email.
    """
    teacher = teachers_collection.find_one({"email": email})
    return teacher

def find_teacher_by_id(teacher_id: str) -> dict:
    """
    Find teacher by id.
    """
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    return teacher

def find_all_teachers() -> list:
    """
    Find all teachers.
    """
    cursor = teachers_collection.find()
    teachers = list(cursor)
    for teacher in teachers:
        teacher["_id"] = str(teacher["_id"])
    return teachers

def insert_new_teacher(teacher: dict) -> dict:
    """
    Insert new teacher.
    """
    result = teachers_collection.insert_one(teacher)
    teacher["_id"] = str(result.inserted_id)
    return teacher

def edit_teacher(teacher_id: str, teacher: dict) -> dict:
    """
    Edit teacher.
    """
    teacher_is_added = find_teacher_by_id(teacher_id)
    if not teacher_is_added:
        raise HTTPException(status_code=400, detail="Teacher does not exist.")
    
    teachers_collection.update_one({"_id": ObjectId(teacher_id)}, {"$set": teacher})
    teacher["_id"] = teacher_id
    return teacher

def delete_teacher(teacher_id: str) -> bool:
    """
    Delete teacher by id.
    """
    result = teachers_collection.delete_one({"_id": ObjectId(teacher_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teacher does not exist.")
    return result.acknowledged
