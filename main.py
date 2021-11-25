import asyncio
from aiogram import executor
from connector import dp
import start_commands
import help_commands
import register_commands
import books_commands
import search

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
