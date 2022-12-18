import asyncio
from aiokafka import AIOKafkaConsumer
import os
from dotenv import load_dotenv

load_dotenv()

message_display_consumer=None
async def consume_message_display(loop:asyncio.AbstractEventLoop):
    message_display_consumer = AIOKafkaConsumer("display_message", bootstrap_servers=os.getenv('KAFKA_INSTANCE'), loop=loop)

    await message_display_consumer.start()

    try:
        async for msg in message_display_consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )

    finally:
        await message_display_consumer.stop()