from pymongo import MongoClient
from test_bot import journalingSystem

view = journalingSystem()
list = view.feeling()
print(
    f"The feeling of the user is {list}"
)

# # Connection credentials
# username = "chibuikeanyiam"
# password = "accessEverton"
#
# # MongoDB connection URL
# url = f"mongodb+srv://{username}:{password}@hackathonbot.96inpog.mongodb.net/?retryWrites=true&w=majority"
#
# # Connect to MongoDB
# myclient = MongoClient(url)
# mydb = myclient["hackathonbot"]
#
# # Choose or create a collection
# mycol = mydb["users"]
#
# # Dummy data to insert
# dummy_users = [
#     {"name": "John Doe", "email": "john@example.com", "age": 25},
#     {"name": "Jane Smith", "email": "jane@example.com", "age": 30},
#     {"name": "Chibuike Anyiam", "email": f"{list}", "age": 22}
# ]
#
# # Insert dummy data
# insert_result = mycol.insert_many(dummy_users)
# print(f"Inserted {len(insert_result.inserted_ids)} documents into 'users' collection.\n")
#
# # Print collections in the database
# print("Collections in 'hackathonbot':", mydb.list_collection_names())
#
# # Retrieve and print all documents from 'users' collection
# print("\nDocuments in 'users' collection:")
# for user in mycol.find():
#     print(user)
#
#
#
