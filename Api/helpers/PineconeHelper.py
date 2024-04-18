from Api.config.db import index
from Api.helpers.embeddingsHelper import get_embedding
from Api.helpers.dateToSecondsHelper import date_string_to_timestamp
from Api.helpers.languageDetectHelper import safe_detect
from Api.helpers.tendersDataCleaningHelper import improve_english_gemini

async def upsert_document_to_pinecone(doc):
    print("Inside: upsert_document_to_pinecone")
    id= str(doc['_id'])
    response = index.fetch(ids=[id])
    if response['vectors']:
        print(f"Document with the id {id} already exists")
        return
    description = doc["AIImprovedDescription"]
    work_type= doc['tenderProductCategory']
    organisation_chain=doc['tenderOrgName']
    areas=doc['AreasByPincode']
    embedding_text=f"{description} - {work_type} - {organisation_chain} - {areas}"
    if description:
        embedding = await get_embedding([embedding_text])

        # Upsert vector into Pinecone
        index.upsert(vectors=[{
            "id": str(doc['_id']),
            "values": embedding,
            "metadata": {
                "tenderOrgName": organisation_chain,
                "tenderRefNumber": doc['tenderRefNumber'],
                "tenderId": doc['tenderId'],
                "tenderCategory": doc['tenderCategory'],
                "tenderCost": doc['tenderCost'],
                "tenderEMDCost": doc['tenderEMDCost'],
                "tenderTitle": doc['tenderTitle'],
                "tenderDescription": doc['tenderDescription'],
                "tenderProductCategory": work_type,
                "tenderBidLocation": doc['tenderBidLocation'],
                "tenderBidStartDate":doc['tenderBidStartDate'],
                "tenderBidEndDate":doc['tenderBidEndDate'],
                "tenderBidStartDateSeconds": date_string_to_timestamp(doc['tenderBidStartDate']),
                "tenderBidEndDateSeconds": date_string_to_timestamp(doc['tenderBidEndDate']),
                "tenderUrl": doc['tenderUrl'],
                "AIImprovedDescription": description,
                'AreasByPincode':areas,
                'DistrictsByPincode':doc['DistrictsByPincode'],
                'StateByPincode':doc['StateByPincode']
            }
        }])
        print(f"Document {doc['_id']} upserted to Pinecone successfully.")

async def query_pinecone(query, top_k=10, emd_min_limit=0, emd_max_limit=2**63 - 1,  
                   bid_start_min='01-Jan-1970 12:00 AM', bid_start_max='31-Dec-9999 12:00 AM', 
                   bid_end_min='01-Jan-1970 12:00 AM', bid_end_max='31-Dec-9999 12:00 AM'):
    
    if not safe_detect(query)=='en':
        query=await improve_english_gemini(query)

    bid_start_min = date_string_to_timestamp(bid_start_min)  
    bid_start_max = date_string_to_timestamp(bid_start_max )  
    bid_end_min = date_string_to_timestamp(bid_end_min)  
    bid_end_max = date_string_to_timestamp(bid_end_max)
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
                {"tenderBidStartDateSeconds": {"$gte": bid_start_min}},
                {"tenderBidStartDateSeconds": {"$lte": bid_start_max}},
                {"tenderBidEndDateSeconds": {"$gte": bid_end_min}},
                {"tenderBidEndDateSeconds": {"$lte": bid_end_max}}
            ]
        }
    )

    # Extract only metadata from Pinecone response matches
    metadata_list = [match['metadata'] for match in response.get('matches', [])]
    return metadata_list
