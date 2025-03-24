import pymongo
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # Đọc URI từ .env
client = pymongo.MongoClient(MONGO_URI)

# Sử dụng database chatbotDB
db = client["chatbotDB"]
