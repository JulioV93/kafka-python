from fastapi import APIRouter, status
from models.message import Message
from schemas.client import producer

router = APIRouter(
    prefix="/producer", 
    tags=["Producer"], 
    responses = {status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: value = {value:12}".format(
            topic=msg.topic(), value=msg.value().decode('utf-8')))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def kafka_producer(msg: Message):
    topic = msg.topic_name

    producer.produce(topic, msg.msg, msg.key, callback=delivery_callback)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()

    return {"message": "Message sent successfully!"}