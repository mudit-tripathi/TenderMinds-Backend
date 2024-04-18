from Api.constant.constants import MIXEDBREAD_API_KEY
from mixedbread_ai.client import MixedbreadAI

# MixedBread AI setup
mxbai = MixedbreadAI(api_key=MIXEDBREAD_API_KEY)

async def get_embedding(texts, model='mixedbread-ai/mxbai-embed-large-v1', prompt=None):
    res = mxbai.embeddings(
        input=texts,
        model=model,
        prompt=prompt
    )
    for entry in res.data:
        if isinstance(entry.embedding, list):
            return entry.embedding
        elif hasattr(entry.embedding, 'float_') and entry.embedding.float_ is not None:
            return entry.embedding.float_
        else:
            raise ValueError("Unsupported embedding format encountered.")