from Api.helpers.PineconeHelper import query_pinecone

async def get_relevant_tenders_from_query(query: str, top_k: int=10, emd_min_limit:float=0, emd_max_limit:float=2**63 - 1,  
                   bid_start:str='01-Jan-1970 12:00 AM',  bid_end:str='31-Dec-9999 12:00 AM'):
    # Call the helper function
    relevant_tenders = await query_pinecone(query, top_k=top_k,emd_min_limit=emd_min_limit,emd_max_limit=emd_max_limit,bid_start=bid_start, bid_end=bid_end)
    return relevant_tenders
