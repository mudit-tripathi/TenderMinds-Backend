from Api.constant.constants import MIXEDBREAD_API_KEY
from mixedbread_ai.client import MixedbreadAI

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

# MixedBread AI setup
mxbai = MixedbreadAI(api_key=MIXEDBREAD_API_KEY)

async def get_embedding(texts, model='mixedbread-ai/mxbai-embed-large-v1', prompt=None):
    logger.info(f"Entered get_embedding helper")
    try:

        res = mxbai.embeddings(
            input=texts,
            model=model,
            prompt=prompt
        )
        for entry in res.data:
            if isinstance(entry.embedding, list):
                return entry.embedding
            elif hasattr(entry.embedding, 'float_') and entry.embedding.float_ is not None:
                logger.info("Exiting get_embedding helper")
                return entry.embedding.float_
            else:
                logger.error("Unsupported embedding format encountered")
                raise ValueError("Unsupported embedding format encountered.")
    
    except Exception as e:
        logger.error("Failed to retrieve embeddings", exc_info=True)
        raise e