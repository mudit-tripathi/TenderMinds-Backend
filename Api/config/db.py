from pymongo import MongoClient
from pinecone import Pinecone
# from Api.config.settings import Settings
import urllib.parse
from Api.constant.constants import PINECONE_API_KEY

# settings = Settings()
username = 'TenderMinds'
password = 'TenderMinds@123'
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@tenderminds.kffghcb.mongodb.net/"

MongoClient = MongoClient(mongo_uri)
db = MongoClient['tenders']

# Pinecone setup
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("tender-minds")