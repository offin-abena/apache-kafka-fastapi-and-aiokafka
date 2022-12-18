from typing import Union

import asyncio
import json
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from dto import MessageRequest

from consumers.display_message import consume_message_display,message_display_consumer

load_dotenv()

from aiokafka import  AIOKafkaProducer

app = FastAPI()

loop:asyncio.AbstractEventLoop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=os.getenv('KAFKA_INSTANCE'))

@app.on_event("startup")
async def startup_event():
    await aioproducer.start()
    loop.create_task(consume_message_display(loop))


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()

    if message_display_consumer:
       await message_display_consumer.stop()


@app.post("/messages/send")
async def kafka_produce(msg: MessageRequest):
    await aioproducer.send('display_message', json.dumps(msg.dict()).encode("ascii"))
    response = MessageRequest(
        title=msg.title, body=msg.body
    )

    return response