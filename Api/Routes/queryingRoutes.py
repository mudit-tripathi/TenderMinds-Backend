from Api.Services import tendersQueryingService as service
from fastapi import APIRouter, Query

tendersQueryingRoutes = APIRouter()
base = '/tenders-search/'

@tendersQueryingRoutes.get(base + "query")
async def search_mongo_ids(query: str, top_n: int = Query(10, description="Number of top results to return")):
    mongo_ids = service.get_mongo_ids_from_query(query, top_n=top_n)
    return mongo_ids