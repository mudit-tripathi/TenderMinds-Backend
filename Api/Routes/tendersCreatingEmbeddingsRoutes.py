from Api.Services import CreatingEmbeddingService as service
from fastapi import APIRouter

tendersCreateEmbeddingRoutes = APIRouter()
base = '/tenders-embedding/'

@tendersCreateEmbeddingRoutes.post(base)
async def createEmbeddings():
    return await service.CreateEmbeddings()