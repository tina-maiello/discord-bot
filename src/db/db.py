from pymongo import MongoClient

client = MongoClient('172.19.96.1',27017)

db = client.discord_bot
col = db['messages']
print(db)

test_dict = {"message_id":"123","message":"321"}

x = col.insert_one(test_dict)