from pymongo import MongoClient


mongo_client = MongoClient('mongodb://localhost:27017/')
if mongo_client:
    print("Connected to MongoDB")
    db = mongo_client['school']
    admins_collection = db['admin']
    students_collection = db['students']
    teachers_collection = db['teachers']
    subjects_collection = db['subjects']
    forms_collection = db['forms']
    streams_collection = db['streams']
    grades_collection = db['grades']
else:
    print("Failed to connect to MongoDB")
