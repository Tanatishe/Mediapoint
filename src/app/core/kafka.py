from aiokafka import AIOKafkaProducer

from src.app.settings.config import settings


async def send_one(data: str):
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    try:
        await producer.send_and_wait(
            topic=settings.kafka_topic, key=settings.kafka_key, value=data
        )
    finally:
        await producer.stop()
