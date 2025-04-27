from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv("data/.env")


client = MongoClient(os.environ.get('DB_SECRET'))

db = client.starboard
col = db['messages']
print(db)

test_dict = {"message_id":"123","message":"321"}

x = col.insert_one(test_dict)