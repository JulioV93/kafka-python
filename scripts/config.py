config = {
    # User-specific properties that you must set
    'bootstrap.servers': 'localhost:9092',

    # Fixed properties
    'group.id':          'kafka-python-getting-started',
    'auto.offset.reset': 'earliest'
}