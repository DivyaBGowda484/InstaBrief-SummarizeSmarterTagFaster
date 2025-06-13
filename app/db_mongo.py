from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.instabrief

def save_document(doc: dict):
    return db.documents.insert_one(doc).inserted_id

def get_document(doc_id: str):
    return db.documents.find_one({"_id": ObjectId(doc_id)})
