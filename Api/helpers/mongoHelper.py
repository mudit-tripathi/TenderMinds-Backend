from Api.config.db import db
from pymongo import ASCENDING
from datetime import datetime

async def insert_processed_tenders(document):
    collection = db['processed-tenders']
    collection.create_index([('tenderRefNumber', ASCENDING)], unique=True)
    existing_tender = collection.find_one({'tenderRefNumber': document['tenderRefNumber']})
    current_time = datetime.now()
    if existing_tender:
        print(f"Tender with Reference Number: {document['tenderRefNumber']} already exists.")
        collection.update_one(
            {"tenderRefNumber": document['tenderRefNumber']},
            {"$set": {"updatedAt": current_time}}
        )
        return None
    try:
        document["createdAt"] = current_time
        document["updatedAt"] = current_time
        print(f"Tender with Reference Number: {document['tenderRefNumber']} inserted successfully.")
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        print(f"An error occurred while inserting the tender: {e}")