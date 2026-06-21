import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
url = f"mongodb+srv://{username}:{password}@hackathonbot.96inpog.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
mydb = client["hackathonbot"]

today = datetime.now().strftime("%Y-%m-%d")

def insert_data_into_profile_collection(interaction_user_id, data):
    collection = mydb["users_new"]

    collection.update_one(
        {
            "user_id": interaction_user_id,
        },
        {
            "$set": data
        },
        upsert=True
    )


def insert_data_into_daily_log_collection(interaction_user_id, data):
    collection = mydb["daily_log"]

    collection.update_one(
        {
            "user_id": interaction_user_id,
            "log_date": today,
        },
        {
            "$set": data
        },
        upsert=True
    )


def insert_data_into_ideation_collection(interaction_user_id, data):
    collection = mydb["brainstorming"]

    collection.update_one(
        {
            "user_id": interaction_user_id,
            "log_date": today,

        },
        {
            "$set": data
        },
        upsert=True
    )