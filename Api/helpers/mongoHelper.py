from Api.config.db import db
from pymongo import ASCENDING
from datetime import datetime

def create_index():
    collection = db['processed-tenders']
    collection.create_index([('tenderId', ASCENDING)], unique=True)

def tender_exists(tenderId):
    collection = db['processed-tenders']
    existing_tender = collection.find_one({'tenderId': tenderId})
    if existing_tender:
        return True
    return False

async def insert_processed_tenders(tender):
    collection = db['processed-tenders']
    current_time = datetime.now()
    if tender_exists(tender['tenderId']):
        print(f"Tender with Tender id Number: {tender['tenderId']} already exists.")
        collection.update_one(
            {"tenderId": tender['tenderId']},
            {"$set": {"updatedAt": current_time}}
        )
        return 
    try:
        tender["createdAt"] = current_time
        tender["updatedAt"] = current_time
        collection.insert_one(tender)
        print(f"Tender with Tender id Number: {tender['tenderId']} inserted successfully.")
    except Exception as e:
        print(f"An error occurred while inserting the tender: {tender['tenderId']} {e}")