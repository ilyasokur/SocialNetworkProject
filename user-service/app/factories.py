from app.service.kafka_producer import KafkaProducerService
from fastapi import Depends
from app.infrastructure.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_kafka_producer(broker_url: str = "localhost:9092") -> KafkaProducerService:
    kafka_producer = KafkaProducerService(broker_url)
    return kafka_producer