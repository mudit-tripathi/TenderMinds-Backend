from Api.helpers.PineconeHelper import query_pinecone

async def get_relevant_tenders_from_query(query: str, top_k: int=10, emd_min_limit:float=0, emd_max_limit:float=2**63 - 1,  
                   bid_start_min:str='01-Jan-1970 12:00 AM', bid_start_max:str='31-Dec-9999 12:00 AM', 
                   bid_end_min:str='01-Jan-1970 12:00 AM', bid_end_max:str='31-Dec-9999 12:00 AM'):
    # Call the helper function
    relevant_tenders = await query_pinecone(query, top_k=top_k,emd_min_limit=emd_min_limit,emd_max_limit=emd_max_limit,bid_start_min=bid_start_min, bid_start_max=bid_start_max, bid_end_min=bid_end_min, bid_end_max=bid_end_max)
    return relevant_tenders
