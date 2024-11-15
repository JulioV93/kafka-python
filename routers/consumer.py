from fastapi import APIRouter, HTTPException, status
from config import config
from models.topic import Topic
from schemas.client import consumer

router = APIRouter(
    prefix="/consumer", 
    tags=["consumer"], 
    responses = {status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

@router.get("/topic/{name}")
async def kafka_data(topic: Topic):
    topic_name = topic.name
    return kafka_consumer(topic_name)

def set_consumer_topics():
    config['enable.auto.commit'] = False

def kafka_consumer(topic_name: str):
    set_consumer_topics()
    # Subscribe to topic
    consumer.subscribe([topic_name])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                return msg.value().decode('utf-8')
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()