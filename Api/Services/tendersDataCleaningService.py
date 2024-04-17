from bson import ObjectId
from Api.config.db import db

from Api.Schemas.serializeObjects import serializeDict, serializeList
from Api.constant.constants import BATCH_SIZE
from Api.helpers.tendersDataCleaningHelper import tendersDataCleaningHelper


async def CleanTenders() -> str:
    pre_processed_tenders_collection = db['pre-processed-tenders']
    pre_processed_tenders_cursor = pre_processed_tenders_collection.find().batch_size(BATCH_SIZE)
    for pre_processed_tenders_document in pre_processed_tenders_cursor:
        print("Inside Loop")
        await tendersDataCleaningHelper(pre_processed_tenders_document)
    total_pre_processed_tenders = pre_processed_tenders_collection.count_documents({})
    return f"{total_pre_processed_tenders} contracts have been cleaned and added to the 'processed-tenders' database."









