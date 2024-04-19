from Api.config.db import db
from pymongo import ASCENDING
from datetime import datetime

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

def create_index():
    collection = db['processed-tenders']
    collection.create_index([('tenderId', ASCENDING)], unique=True)
    

def tender_exists(tenderId):
    logger.info("Entered tender_exists function")
    collection = db['processed-tenders']
    existing_tender = collection.find_one({'tenderId': tenderId})
    if existing_tender:
        return True
    return False

async def insert_processed_tenders(tender):
    logger.info("Entered insert_processed_tenders")
    collection = db['processed-tenders']
    current_time = datetime.now()
    if tender_exists(tender['tenderId']):
        logger.info(f"Tender with Tender id Number: {tender['tenderId']} already exists.")
        collection.update_one(
            {"tenderId": tender['tenderId']},
            {"$set": {"updatedAt": current_time}}
        )
        return 
    try:
        tender["createdAt"] = current_time
        tender["updatedAt"] = current_time
        collection.insert_one(tender)
        logger.info(f"Tender with Tender id Number: {tender['tenderId']} inserted successfully.")
    except Exception as e:
        logger.error(f"An error occurred while inserting the tender: {tender['tenderId']} {e}")