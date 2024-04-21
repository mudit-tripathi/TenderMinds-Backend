from bson import ObjectId
from Api.config.db import db

from Api.Schemas.serializeObjects import serializeDict, serializeList
from Api.constant.constants import BATCH_SIZE
from Api.helpers.tendersDataCleaningHelper import tendersDataCleaningHelper

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

async def CleanTenders() -> str:
    logger.info("Entered CleanTenders service")
    pre_processed_tenders_collection = db['pre-processed-tenders']
    pre_processed_tenders_cursor = pre_processed_tenders_collection.find().batch_size(BATCH_SIZE)
    count=0
    for pre_processed_tenders_document in pre_processed_tenders_cursor:
        if count==200:
            break
        await tendersDataCleaningHelper(pre_processed_tenders_document)
        count+=1
    logger.info(f"{count} contracts have been cleaned and added to the 'processed-tenders' database.")










