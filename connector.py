from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
from pymongo import MongoClient


MAX_elements = 100
CONNECTION_STRING = ""

client = motor.motor_asyncio.AsyncIOMotorClient(
    CONNECTION_STRING, uuidRepresentation="standard"
)

pym_client = MongoClient("mongodb+srv://pakrentos:kyh63r8l48@bookfriendingapp.nme65.mongodb.net/test")
pym_db = pym_client.test

contact_info = {}
contact_info_mapping = ["name", "age", "location", "gender"]
book_info = {}
matches_info = {}

db = client["test"]
user_collection = db["tg_users"]
book_collection = db["books"]


API_TOKEN = '2141280047:AAHsAq3iDUQ9rSRyy43BQV0rzgsHp55Uq-M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
