from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio

CONNECTION_STRING = "mongodb+srv://pakrentos:kyh63r8l48@bookfriendingapp.nme65.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(
    CONNECTION_STRING, uuidRepresentation="standard"
)

contact_info = {}
contact_info_mapping = ["name", "age", "location", "gender"]
book_info = {}

db = client["test"]
user_collection = db["tg_users"]
book_collection = db["books"]


API_TOKEN = '2141280047:AAHsAq3iDUQ9rSRyy43BQV0rzgsHp55Uq-M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
