import asyncio
import logging
import sys
from aiogram.client.bot import Bot
from aiogram import Dispatcher
from config import settings
from routers import base_router, ai_router
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage  # ← ВАЖНО!

redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
storage = RedisStorage(redis=redis_client)

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=settings.BOT_TOKEN)

    dispatcher = Dispatcher(storage=storage)
    dispatcher.include_router(base_router)
    dispatcher.include_router(ai_router)

    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
