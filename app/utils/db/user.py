from fastapi import HTTPException, status

from app.db.mongo_db import user_index


def user_added_to_index(identifier: str, role: str) -> bool:
    """
    Add a user for indexing.
    """
    user_is_added = get_user_by_identifier(identifier)
    if user_is_added:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with similar email or admission number already exists.")
    user = {
        "_id": identifier,
        "role": role
    }
    result = user_index.insert_one(user)
    return result.acknowledged

def get_user_by_identifier(identifier: str):
    """
    Get user by email or admission number.
    """
    user = user_index.find_one({"_id": identifier})
    return user
