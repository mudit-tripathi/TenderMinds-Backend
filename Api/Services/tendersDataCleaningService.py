from bson import ObjectId
from Api.config.db import db

from Api.Schemas.serializeObjects import serializeDict, serializeList
from Api.constant.constants import BATCH_SIZE

from Api.helpers.tendersDataCleaningHelper import improve_english_gemini
from Api.helpers.tendersDataCleaningHelper import contract_info


async def clean_tender_description(tender):
    return improve_english_gemini(tender)

async def update_contract_info_service(tender):
    return contract_info(tender)

async def CleanTenders() -> str:
    pre_processed_tenders_collection = db['pre-processed-tenders']
    pre_processed_tenders_cursor = pre_processed_tenders_collection.find().batch_size(BATCH_SIZE)
    total_pre_processed_tenders_tenders = pre_processed_tenders_collection.count_documents({})
    total_processed = 0
    for pre_processed_tenders_document in pre_processed_tenders_cursor:
        print(pre_processed_tenders_document)
        break
    return total_pre_processed_tenders_tenders









