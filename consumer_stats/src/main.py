import sys
print(sys.path)
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError


logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

lang_counter = {}
sentiment_counter = {}


def msg_process(msg):
    message_value = str(msg.value())
    topic = str(msg.topic())
    logger.info(f"{message_value}    {topic}")

    if topic == "languages-topic":
        if message_value in lang_counter:
            lang_counter[message_value] += 1
        else:
            lang_counter[message_value] = 1
        logger.info(lang_counter)

    if topic == "sentiment-topic":
        if message_value in sentiment_counter:
            sentiment_counter[message_value] += 1
        else:
            sentiment_counter[message_value] = 1
        logger.info(sentiment_counter)


def basic_consume_loop(consumer, topics):
    try:

        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


if __name__ == '__main__':

    conf = {'bootstrap.servers': 'kafka-1:9092',
            'group.id': "language_group",
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'}

    consumer = Consumer(conf)
    running = True
    basic_consume_loop(consumer, ["languages-topic", "sentiment-topic"])
    shutdown()
