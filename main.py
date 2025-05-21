import asyncio
import logging
import sys
from aiogram.client.bot import Bot
from aiogram import Dispatcher
from config import settings
from kafka_settings.consumer import consume_results
from kafka_settings.producer import start_producer, stop_producer
from routers import base_router, ai_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=settings.BOT_TOKEN)
    await start_producer()
    asyncio.create_task(consume_results(bot=bot))
    dispatcher = Dispatcher()
    dispatcher.include_router(base_router)
    dispatcher.include_router(ai_router)

    try:
        await dispatcher.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка запуска бота: ${e}")
    finally:
        await stop_producer()


if __name__ == '__main__':
    asyncio.run(main())
