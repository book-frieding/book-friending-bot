from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
from pymongo import MongoClient


MAX_elements = 100
CONNECTION_STRING = "mongodb+srv://pakrentos:kyh63r8l48@bookfriendingapp.nme65.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(
    CONNECTION_STRING, uuidRepresentation="standard"
)

pym_client = MongoClient("mongodb+srv://pakrentos:kyh63r8l48@bookfriendingapp.nme65.mongodb.net/test")
pym_db = pym_client.test

contact_info = {}
contact_info_mapping = ["name", "age", "location", "gender"]
book_info = {}

db = client["test"]
user_collection = db["tg_users"]
book_collection = db["books"]


API_TOKEN = '2130902396:AAGUsSStMj_5UfQZqvklgo1A6UKPizYmAvI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
