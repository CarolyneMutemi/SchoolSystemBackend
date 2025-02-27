from pymongo import ReturnDocument

from app.db.mongo_db import results_collection


def add_or_update_subject_results(result: dict):
    search_query = {
            "student_adm_no": result.get("student_adm_no"),
            "year": result.get("year"),
            "term": result.get("term"),
            "form": result.get("form"),  # Update form
            "stream": result.get("stream").lower(),  # Update stream
            "subject_results.subject": result.get("subject").upper()  # Check if subject exists
        }
    existing_record = results_collection.find_one(search_query)

    if existing_record:
        # Subject exists: Update the marks and grade
        update_query = {
            "$set": {
                f"subject_results.$.marks": result.get("marks"),  # Update marks
                f"subject_results.$.grade": result.get("grade")  # Update grade
            }
        }
    else:
        # Subject does not exist: Add new subject to subject_results array
        update_query = {
            "$push": {
                "subject_results": {
                    "subject": result.get("subject"),
                    "marks": result.get("marks"),
                    "grade": result.get("grade")
                }
            }
        }

    # Upsert: Create document if not found, update if found
    if not existing_record:
        search_query.pop("subject_results.subject")
    db_result = results_collection.find_one_and_update(
        search_query,
        update_query,
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    db_result.pop("_id")

    return db_result

def get_all_subject_results(subject: str, year: int, form: int, stream: str) -> list:
    """
    Get all student subject results in a year.
    """
    cursor = results_collection.find({"year": year, "subject_results.subject": subject.upper(), "form": form, "stream": stream.lower()}).sort("subject_results.marks", -1)
    results = list(cursor)
    for result in results:
        result.pop("_id")
    return results
