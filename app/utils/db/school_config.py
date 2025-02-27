from fastapi import HTTPException
from bson import ObjectId

from app.db.mongo_db import grades_collection, subjects_collection, forms_collection, streams_collection


def add_grade(grade: dict) -> dict:
    """
    Add grade.
    """
    grade_is_added = find_grade_by_name(grade["letter"])
    if grade_is_added:
        raise HTTPException(status_code=400, detail="Grade already exists.")
    result = grades_collection.insert_one(grade)
    grade["_id"] = str(result.inserted_id)
    return grade

def find_grade_by_name(letter: str) -> dict:
    """
    Find grade by letter.
    """
    grade = grades_collection.find_one({"letter": letter})
    return grade

def find_grade_by_id(grade_id: str) -> dict:
    """
    Find grade by id.
    """
    grade = grades_collection.find_one({"_id": ObjectId(grade_id)})
    return grade

def find_all_grades() -> list:
    """
    Find all grades.
    """
    cursor = grades_collection.find()
    grades = list(cursor)
    for grade in grades:
        grade["_id"] = str(grade["_id"])
    return grades

def edit_grade(grade_id: str, grade: dict) -> dict:
    """
    Edit grade.
    """
    grade_is_added = find_grade_by_id(grade_id)
    if not grade_is_added:
        raise HTTPException(status_code=400, detail="Grade does not exist.")
    
    grades_collection.update_one({"_id": ObjectId(grade_id)}, {"$set": grade})
    return grade

def delete_grade(grade_id: str) -> bool:
    """
    Delete grade by id.
    """
    result = grades_collection.delete_one({"_id": ObjectId(grade_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Grade does not exist.")
    return result.acknowledged

def add_subject(subject: dict) -> dict:
    """
    Add subject.
    """
    subject_is_added = find_subject_by_code(subject["code"])
    if subject_is_added:
        raise HTTPException(status_code=400, detail="Subject already exists.")
    subject["code"] = subject["code"].upper()
    result = subjects_collection.insert_one(subject)
    subject["_id"] = str(result.inserted_id)
    return subject

def find_subject_by_code(code: str) -> dict:
    """
    Find subject by code.
    """
    subject = subjects_collection.find_one({"code": code.upper()})
    return subject

def find_all_subjects() -> list:
    """
    Find all subjects.
    """
    cursor = subjects_collection.find()
    subjects = list(cursor)
    for subject in subjects:
        subject["_id"] = str(subject["_id"])
    return subjects

def find_subject_by_id(subject_id: str) -> dict:
    """
    Find subject by id.
    """
    subject = subjects_collection.find_one({"_id": ObjectId(subject_id)})
    return subject

def edit_subject(subject_id: str, subject: dict) -> dict:
    """
    Edit subject.
    """
    subject_is_added = find_subject_by_id(subject_id)
    if not subject_is_added:
        raise HTTPException(status_code=400, detail="Subject does not exist.")
    
    subjects_collection.update_one({"_id": ObjectId(subject_id)}, {"$set": subject})
    return subject

def delete_subject(subject_id: str) -> bool:
    """
    Delete subject by id.
    """
    result = subjects_collection.delete_one({"_id": ObjectId(subject_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subject does not exist.")
    return result.acknowledged

def add_form(form: dict) -> dict:
    """
    Add form.
    """
    form_is_added = find_form_by_level(form["level"])
    if form_is_added:
        raise HTTPException(status_code=400, detail="Form already exists.")
    result = forms_collection.insert_one(form)
    form["_id"] = str(result.inserted_id)
    return form

def find_form_by_level(level: int) -> dict:
    """
    Find form by name.
    """
    form = forms_collection.find_one({"level": level})
    return form

def find_all_forms() -> list:
    """
    Find all forms.
    """
    cursor = forms_collection.find()
    forms = list(cursor)
    for form in forms:
        form["_id"] = str(form["_id"])
    return forms

def find_form_by_id(form_id: str) -> dict:
    """
    Find form by id.
    """
    form = forms_collection.find_one({"_id": ObjectId(form_id)})
    return form

def edit_form(form_id: str, form: dict) -> dict:
    """
    Edit form.
    """
    form_is_added = find_form_by_id(form_id)
    if not form_is_added:
        raise HTTPException(status_code=400, detail="Form does not exist.")
    
    result = forms_collection.update_one({"_id": ObjectId(form_id)}, {"$set": form})
    return form

def delete_form(form_id: str) -> bool:
    """
    Delete form by id.
    """
    result = forms_collection.delete_one({"_id": ObjectId(form_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Form does not exist.")
    return result.acknowledged

def add_stream(stream: dict) -> dict:
    """
    Add stream.
    """
    stream_is_added = find_stream_by_name(stream["name"])
    print("Is stream added: ", stream_is_added)
    if stream_is_added:
        raise HTTPException(status_code=400, detail="Stream already exists.")
    stream["name"] = stream["name"].lower()
    result = streams_collection.insert_one(stream)
    stream["_id"] = str(result.inserted_id)
    return stream

def find_stream_by_name(name: str) -> dict:
    """
    Find stream by name.
    """
    stream = streams_collection.find_one({"name": name.lower()})
    print("Stream: ", stream)
    return stream

def find_all_streams() -> list:
    """
    Find all streams.
    """
    cursor = streams_collection.find()
    streams = list(cursor)
    for stream in streams:
        stream["_id"] = str(stream["_id"])
    return streams

def find_stream_by_id(stream_id: str) -> dict:
    """
    Find stream by id.
    """
    stream = streams_collection.find_one({"_id": ObjectId(stream_id)})
    return stream

def edit_stream(stream_id: str, stream: dict) -> dict:
    """
    Edit stream.
    """
    stream_is_added = find_stream_by_id(stream_id)
    if not stream_is_added:
        raise HTTPException(status_code=400, detail="Stream does not exist.")
    
    streams_collection.update_one({"_id": ObjectId(stream_id)}, {"$set": stream})
    return stream

def delete_stream(stream_id: str) -> bool:
    """
    Delete stream by id.
    """
    result = streams_collection.delete_one({"_id": ObjectId(stream_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Stream does not exist.")
    return result.acknowledged
