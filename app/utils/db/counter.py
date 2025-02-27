from pymongo import ReturnDocument
from app.db.mongo_db import counters_collection

def initialize_counter():
    """Initialize the admission counter if it does not exist."""
    existing_counter = counters_collection.find_one({"_id": "admission_number"})
    if not existing_counter:
        counters_collection.insert_one({"_id": "admission_number", "sequence_value": 1000})  # Start from 1000

def get_next_admission_number():
    """Atomically increments and returns the next admission number."""
    result = counters_collection.find_one_and_update(
        {"_id": "admission_number"},
        {"$inc": {"sequence_value": 1}},  # Increment by 1
        return_document=ReturnDocument.AFTER
    )
    return result["sequence_value"]
