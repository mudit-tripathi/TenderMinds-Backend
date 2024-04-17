from Api.config.db import db
from pymongo import ASCENDING
from datetime import datetime

def create_index():
    collection = db['processed-tenders']
    collection.create_index([('tenderId', ASCENDING)], unique=True)

async def insert_processed_tenders(document):
    collection = db['processed-tenders']
    existing_tender = collection.find_one({'tenderId': document['tenderId']})
    current_time = datetime.now()
    if existing_tender:
        print(f"Tender with Tender id Number: {document['tenderId']} already exists.")
        collection.update_one(
            {"tenderId": document['tenderId']},
            {"$set": {"updatedAt": current_time}}
        )
        return None
    try:
        document["createdAt"] = current_time
        document["updatedAt"] = current_time
        result = collection.insert_one(document)
        print(f"Tender with Tender id Number: {document['tenderId']} inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting the tender: {document['tenderId']} {e}")