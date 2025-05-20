import base64
import json
from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    await producer.start()

async def stop_producer():
    global producer
    if producer:
        await producer.stop()

async def send_prompt(prompt: str, user_id: int, chat_id: int):
    if not producer:
        raise RuntimeError("Kafka producer not started")
    await producer.send("drawing-prompt", value={
        "prompt": prompt,
        "user_id": user_id,
        "chat_id": chat_id
    })

async def send_image(image_bytes: bytes, user_id: int, chat_id: int):
    if not producer:
        raise RuntimeError("Kafka producer not started")
    await producer.send("drawing-image", value={
        "image": base64.b64encode(image_bytes).decode('utf-8'),
        "user_id": user_id,
        "chat_id": chat_id
    })
