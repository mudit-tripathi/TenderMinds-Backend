from fastapi import APIRouter, Query, HTTPException
from Api.Services import tendersQueryingService as service

tendersQueryingRoutes = APIRouter()
base = '/tenders-search/'

@tendersQueryingRoutes.get(base + "query")
async def search_tenders(query: str, top_k: int = Query(10, description="Number of top results to return"),
                     emd_min_limit: float = Query(0, description="Minimum EMD limit"),
                     emd_max_limit: float = Query(2**63 - 1, description="Maximum EMD limit"),
                     bid_start_min: str = Query('01-Jan-1970 12:00 AM', description="Minimum bid submission start date"),
                     bid_start_max: str = Query('31-Dec-9999 12:00 AM', description="Maximum bid submission start date"),
                     bid_end_min: str = Query('01-Jan-1970 12:00 AM', description="Minimum bid submission end date"),
                     bid_end_max: str = Query('31-Dec-9999 12:00 AM', description="Maximum bid submission end date")):
    
    relevant_tenders = await service.get_relevant_tenders_from_query(
        query, top_k=top_k, emd_min_limit=emd_min_limit, emd_max_limit=emd_max_limit,
        bid_start_min=bid_start_min, bid_start_max=bid_start_max,
        bid_end_min=bid_end_min, bid_end_max=bid_end_max
    )
    return relevant_tenders