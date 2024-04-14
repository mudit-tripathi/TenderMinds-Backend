from bson import ObjectId
from Api.config.db import db

from Api.Schemas.serializeObjects import serializeDict, serializeList
from Api.constant.constants import BATCH_SIZE

from Api.helpers.tendersDataCleaningHelper import improve_english_gemini
from Api.helpers.tendersDataCleaningHelper import contract_info


async def clean_tender_description(tender):
    return improve_english_gemini(tender)

async def get_contract_summary(tender):
    return contract_info(tender)

async def CleanTenders() -> str:
    pre_processed_tenders_collection = db['pre-processed-tenders']
    pre_processed_tenders_cursor = pre_processed_tenders_collection.find().batch_size(BATCH_SIZE)
    total_pre_processed_tenders_tenders = pre_processed_tenders_collection.count_documents({})
    total_processed = 0
    for pre_processed_tenders_document in pre_processed_tenders_cursor:
        clean_tender_description(pre_processed_tenders_document)
        get_contract_summary(pre_processed_tenders_document)
       
    return total_pre_processed_tenders_tenders









