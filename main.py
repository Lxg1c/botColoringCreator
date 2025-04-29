import asyncio
import logging
import sys
from aiogram.client.bot import Bot
from aiogram import Dispatcher
from config import settings
from routers import base_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=settings.BOT_TOKEN)

    dispatcher = Dispatcher()
    dispatcher.include_router(base_router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
