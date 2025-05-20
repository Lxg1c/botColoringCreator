import json
import asyncio
from aiokafka import AIOKafkaConsumer
from aiogram.types import BufferedInputFile
import base64
from shared import logger


async def consume_results(bot):
    while True:  # Бесконечный цикл для переподключения
        consumer = AIOKafkaConsumer(
            "drawing-result",
            bootstrap_servers='kafka:9092',
            group_id='tg-bot',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=300000
        )

        try:
            await consumer.start()
            logger.info("Kafka consumer successfully started")

            async for msg in consumer:
                try:
                    data = msg.value
                    image_bytes = base64.b64decode(data['image'])
                    await bot.send_photo(
                        chat_id=data['chat_id'],
                        photo=BufferedInputFile(image_bytes, "result.png"),
                        caption="Ваш результат готов!"
                    )
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Kafka connection error: {e}, reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        finally:
            await consumer.stop()
