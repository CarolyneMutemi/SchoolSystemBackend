from fastapi import HTTPException
from bson import ObjectId

from app.db.mongo_db import admins_collection


def find_admin_by_email(email: str) -> dict:
    """
    Find admin by email.
    """
    admin = admins_collection.find_one({"email": email})
    if not admin:
        return None
    admin["_id"] = str(admin["_id"])
    return admin

def find_admin_by_id(admin_id: str) -> dict:
    """
    Find admin by id.
    """
    admin = admins_collection.find_one({"_id": ObjectId(admin_id)})
    if not admin:
        return None

    admin["_id"] = str(admin["_id"])
    return admin

def find_all_admins() -> list:
    """
    Find all admins.
    """
    cursor = admins_collection.find()
    admins = list(cursor)
    for admin in admins:
        admin["_id"] = str(admin["_id"])
        del admin["password"]
    return admins

def insert_new_admin(admin: dict) -> bool:
    """
    Insert new admin.
    """
    result = admins_collection.insert_one(admin)
    return result.acknowledged

def edit_admin(admin_id: str, admin: dict) -> dict:
    """
    Edit admin.
    """
    admin_is_added = find_admin_by_id(admin_id)
    if not admin_is_added:
        raise HTTPException(status_code=400, detail="Admin does not exist.")
    
    admins_collection.update_one({"_id": ObjectId(admin_id)}, {"$set": admin})
    admin["_id"] = admin_id
    return admin

def delete_admin(id: str) -> bool:
    """
    Delete admin by id.
    """
    result = admins_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin does not exist.")
    return result.acknowledged


