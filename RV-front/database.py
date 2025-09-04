import motor.motor_asyncio
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://root:password@localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.plant_disease_db

user_collection = database.get_collection("users")
prediction_collection = database.get_collection("predictions")