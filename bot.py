import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config

from handlers.handlers import router

#Turn on logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.api_token.get_secret_value())

dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())