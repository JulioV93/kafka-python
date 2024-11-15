from confluent_kafka import Producer
from config import config

# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: value = {value:12}".format(
            topic=msg.topic(), value=msg.value().decode('utf-8')))

if __name__ == '__main__':
    topic_name = input("Introduce el nombre del topic: ")
    message = input("Introduce el mensaje: ")

    producer = Producer(config)

    producer.produce(topic_name, message, callback=delivery_callback)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()