from confluent_kafka import Consumer, KafkaException
from config import config

def set_consumer_topics():
    config['group.id'] = 'hello_group'
    config['auto.offset.reset'] = 'earliest'
    config['enable.auto.commit'] = False

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic} partition {p.partition}')

if __name__ == '__main__':
    topic_name = input("Introduce el nombre del topic: ")

    set_consumer_topics()
    consumer = Consumer(config)
    consumer.subscribe([topic_name], on_assign=assignment_callback)
    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                print("Waiting...")
                continue
            if event.error():
                if event.error().code() == KafkaException._PARTITION_EOF:
                    print(f'End of partition reached {event.topic()}[{event.partition()}] offset {event.offset()}')
                else:
                    raise KafkaException(event.error())
            else:
                print(f'{event.value().decode("utf-8")} from partition {event.partition()}')
                #consumer.commit(event)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()