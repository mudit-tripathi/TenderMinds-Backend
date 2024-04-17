from Api.config.db import index
from Api.helpers.embeddingsHelper import get_embedding

async def upsert_document_to_pinecone(doc):
    description = doc.get("AIContractSummary")  
    if description:
        embedding = get_embedding([description])

        # Upsert vector into Pinecone
        index.upsert(vectors=[{
            "id": str(doc['_id']),
            "values": embedding,
            "metadata": {
                "tenderOrgName": doc['tenderOrgName'],
                "tenderRefNumber": doc['tenderRefNumber'],
                "tenderId": doc['tenderId'],
                "tenderCategory": doc['tenderCategory'],
                "tenderCost": doc['tenderCost'],
                "tenderEMDCost": doc['tenderEMDCost'],
                "tenderTitle": doc['tenderTitle'],
                "tenderDescription": doc['tenderDescription'],
                "tenderProductCategory": doc['tenderProductCategory'],
                "tenderBidLocation": doc['tenderBidLocation'],
                "tenderBidStartDate": doc['tenderBidStartDate'],
                "tenderBidEndDate": doc['tenderBidEndDate'],
                "tenderUrl": doc['tenderUrl'],
                "AIImprovedDescription": doc.get('AIImprovedDescription'),
                "LocationByPincode": doc.get('LocationByPincode'),
                "AIContractSummary": doc.get('AIContractSummary')
            }
        }])
        print(f"Document {doc['_id']} upserted to Pinecone successfully.")

def query_pinecone_for_mongoids(query, top_k=10):
    # Get embedding for the query
    vector = get_embedding(query)

    # Query Pinecone
    response = index.query(
        vector=vector,
        top_k=top_k,
        include_values=False,
        include_metadata=False
    )

    # Extract MongoDB IDs from Pinecone response
    match_ids = [match['id'] for match in response.get('matches', [])]
    return match_ids
