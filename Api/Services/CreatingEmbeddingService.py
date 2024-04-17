from Api.config.db import db
from Api.constant.constants import BATCH_SIZE
from Api.helpers.PineconeHelper import upsert_document_to_pinecone


async def CreateEmbeddings() -> str:
    processed_tenders_collection = db['processed-tenders']
    processed_tenders_cursor = processed_tenders_collection.find().batch_size(BATCH_SIZE)
    count=0
    for processed_tenders_document in processed_tenders_cursor:
        print("Inside Loop")
        await upsert_document_to_pinecone(processed_tenders_document)
        count+=1
    return f"Embeddings have been created and inserted to Pinecone for {count} contracts"
