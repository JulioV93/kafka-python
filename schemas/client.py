from confluent_kafka.admin import (AdminClient)
from confluent_kafka import Consumer, Producer
from config import config

# Create Admin client
# The AdminClient is used to perform administrative operations on the Kafka cluster.
admin = AdminClient(config)

# Create Consumer instance
consumer = Consumer(config)

# Create Producer instance
producer = Producer(config)