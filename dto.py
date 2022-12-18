from pydantic import BaseModel
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

class MessageRequest(BaseModel):
    title: str
    body: str
