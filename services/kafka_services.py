from confluent_kafka.admin import (AdminClient, NewTopic, ConfigResource, KafkaException)
from config import config

# return True if topic exists and False if not
def topic_exists(admin, topic):
    metadata = admin.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False

# create new topic and return results dictionary
def create_topic(admin, topic, max_msg_k):
    new_topic = NewTopic(topic, num_partitions=6, replication_factor=1) 
    result_dict = admin.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            
            # Check max.message.bytes config and set if needed
            current_max = get_max_size(admin, topic)
            if current_max != str(max_msg_k * 1024):
                print(f'Topic, {topic} max.message.bytes is {current_max}.')
                set_max_size(admin, topic, max_msg_k)

            # Verify config was set 
            new_max = get_max_size(admin, topic)
            print(f'Now max.message.bytes for topic {topic} is {new_max}')

            print("Topic {} created".format(topic))
        except KafkaException as e:
            print("Failed to create topic {}: {}".format(topic, e))
        except Exception as e:
            print("An error occurred: {}".format(e))
        except ValueError as e:
            print("ValueError: {}".format(e))

# get max.message.bytes property
def get_max_size(admin, topic):
    resource = ConfigResource('topic', topic)
    result_dict = admin.describe_configs([resource])
    config_entries = result_dict[resource].result()
    max_size = config_entries['max.message.bytes']
    return max_size.value

# set max.message.bytes for topic
def set_max_size(admin, topic, max_k):
    config_dict = {'max.message.bytes': str(max_k*1024)}
    resource = ConfigResource('topic', topic, config_dict)
    result_dict = admin.incremental_alter_configs([resource])
    result_dict[resource].result()

def get_topics(admin):
    topics = admin.list_topics()
    return topics.topics

def search_topic(admin, topic_name):
    topics = admin.list_topics(topic_name)
    return topics.topics

def delete_topics(admin, topic_name):
    # Delete topic if it exists
    admin.delete_topics([topic_name])

def update_topic(admin, topic_name, max_msg_k):
    # Update topic if it exists
    set_max_size(admin, topic_name, max_msg_k)
