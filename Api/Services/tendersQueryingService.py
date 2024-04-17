from Api.helpers.PineconeHelper import query_pinecone_for_mongoids

def get_mongo_ids_from_query(query: str, top_n: int = 10):
    # Call the helper function
    mongo_ids = query_pinecone_for_mongoids(query, top_k=top_n)
    return mongo_ids