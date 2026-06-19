import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# print(
#     f"The feeling of the user is {user}"
# )

url = f"mongodb+srv://{username}:{password}@hackathonbot.96inpog.mongodb.net/?retryWrites=true&w=majority"


myclient = MongoClient(url)
mydb = myclient["hackathonbot"]


mycol = mydb["users"]
new_my_col = mydb["usersnew"]

# mycol.delete_many({})
#
#
# dummy_users = [
#     {"name": "John Doe", "email": "john@example.com", "age": 25},
#     {"name": "Jane Smith", "email": "jane@example.com", "age": 30},
#     {"name": "Chibuike Anyiam", "email": f"{list}", "age": 22}
# ]
#
#
# insert_result = mycol.insert_many(dummy_users)
# print(f"Inserted {len(insert_result.inserted_ids)} documents into 'users' collection.\n")
#
#
# print("Collections in 'hackathonbot':", mydb.list_collection_names())

#
# print("\nDocuments in 'users' collection:")
# for user in mycol.find():
#     print(user)