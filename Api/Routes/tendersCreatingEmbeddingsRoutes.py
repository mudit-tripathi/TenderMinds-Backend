from Api.Services import CreatingEmbeddingService as service
from fastapi import APIRouter

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

tendersCreateEmbeddingRoutes = APIRouter()
base = '/tenders-embedding/'

@tendersCreateEmbeddingRoutes.post(base)
async def createEmbeddings():
    return await service.CreateEmbeddings()