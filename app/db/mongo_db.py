from pymongo import MongoClient


mongo_client = MongoClient('mongodb://localhost:27017/')
if mongo_client:
    print("Connected to MongoDB")
    db = mongo_client['school']
    user_index = db["user_index"]
    admins_collection = db['admin']
    students_collection = db['students']
    teachers_collection = db['teachers']
    subjects_collection = db['subjects']
    forms_collection = db['forms']
    streams_collection = db['streams']
    grades_collection = db['grades']
    results_collection = db['results']
    counters_collection = db['counters']

    # Create indexes
    results_collection.create_index(
    [("student_adm_no", 1), ("year", 1), ("term", 1), ("subject_results.subject", 1)],
    unique=True
)
else:
    print("Failed to connect to MongoDB")
