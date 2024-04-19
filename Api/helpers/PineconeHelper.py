from Api.config.db import index
from Api.helpers.embeddingsHelper import get_embedding
from Api.helpers.dateToSecondsHelper import date_string_to_timestamp
from Api.helpers.languageDetectHelper import safe_detect
from Api.helpers.tendersDataCleaningHelper import improve_english_gemini
from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

async def upsert_document_to_pinecone(doc):
    logger.info("Entered upsert_document_to_pinecone function ")
    id= str(doc['_id'])
    response = index.fetch(ids=[id])
    if response['vectors']:
        logger.info(f"Document with the id {id} already exists")
        return
    description = doc["AIImprovedDescription"]
    work_type= doc['tenderProductCategory']
    organisation_chain=doc['tenderOrgName']
    areas=doc['AreasByPincode']
    districts=doc['DistrictsByPincode']
    state=doc['StateByPincode']

    embedding_text=f"DESCRIPTION: {description} - WORK_TYPE: {work_type} - ORG: {organisation_chain} - AREAS: {areas} - DISTRICTS: {districts} - STATE: {state}"
    logger.info(f"Length of the embedding_text: {len(embedding_text)}")
    embedding = await get_embedding([embedding_text])

    # Upsert vector into Pinecone
    index.upsert(vectors=[{
        "id": str(doc['_id']),
        "values": embedding,
        "metadata": {
            "tenderOrgName": organisation_chain,
            "tenderProductCategory": work_type,
            "AIImprovedDescription": description,
            'AreasByPincode':areas,
            'DistrictsByPincode':districts,
            'StateByPincode':state,
            "tenderRefNumber": doc['tenderRefNumber'],
            "tenderId": doc['tenderId'],
            "tenderCategory": doc['tenderCategory'],
            "tenderCost": doc['tenderCost'],
            "tenderEMDCost": doc['tenderEMDCost'],
            "tenderTitle": doc['tenderTitle'],
            "tenderDescription": doc['tenderDescription'],
            "tenderBidLocation": doc['tenderBidLocation'],
            "tenderBidStartDate":doc['tenderBidStartDate'],
            "tenderBidEndDate":doc['tenderBidEndDate'],
            "tenderBidStartDateSeconds": date_string_to_timestamp(doc['tenderBidStartDate']),
            "tenderBidEndDateSeconds": date_string_to_timestamp(doc['tenderBidEndDate']),
            "tenderUrl": doc['tenderUrl']
            
        }
    }])
    logger.info(f"Document {doc['_id']} upserted to Pinecone successfully.")

async def query_pinecone(query, top_k=10, emd_min_limit=0, emd_max_limit=2**63 - 1,  
                   bid_start='01-Jan-1970 12:00 AM', bid_end='31-Dec-9999 12:00 AM'):
    
    logger.info("Entered query_pinecone function")
    if not safe_detect(query)=='en':
        query=await improve_english_gemini(query)

    bid_start = date_string_to_timestamp(bid_start)   
    bid_end = date_string_to_timestamp(bid_end)
    # Get embedding for the query
    vector = await get_embedding(query)

    # Adjust Pinecone query to use a realistic high value instead of infinity
    response = index.query(
        vector=vector,
        top_k=top_k,
        include_values=False,
        include_metadata=True,
        filter={
            "$and": [
                {"tenderEMDCost": {"$gte": emd_min_limit}},
                {"tenderEMDCost": {"$lte": emd_max_limit}},
                {"tenderBidStartDateSeconds": {"$gte": bid_start}},
                {"tenderBidEndDateSeconds": {"$lte": bid_end}}
            ]
        }
    )

    # Extract only metadata from Pinecone response matches
    metadata_list = [{'score': match['score'], 'metadata': match['metadata']} for match in response.get('matches', [])]

    logger.info("Exiting query_pinecone function")
    return metadata_list
