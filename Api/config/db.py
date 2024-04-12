from pymongo import MongoClient
# from Api.config.settings import Settings
import urllib.parse

# settings = Settings()
username = 'TenderMinds'
password = 'TenderMinds@123'
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)
mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@tenderminds.kffghcb.mongodb.net/"

MongoClient = MongoClient(mongo_uri)
db = MongoClient['tenders']