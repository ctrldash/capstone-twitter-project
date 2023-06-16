import sys
print(sys.path)
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError
from sentiment_analysator import SentimentAnalysator


logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


def msg_process(msg, analyzer):
    logger.info(msg.value())

    msg_sentiment = analyzer.run(str(msg.value()))

    logger.info(msg_sentiment)


def basic_consume_loop(consumer, topics):
    try:
        sentiment_analysator = SentimentAnalysator()

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
                msg_process(msg, sentiment_analysator)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


if __name__ == '__main__':

    conf = {'bootstrap.servers': 'kafka-1:9092',
            'group.id': "sentiment_group",
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'}

    consumer = Consumer(conf)
    running = True
    basic_consume_loop(consumer, ["tweets-topic"])
    shutdown()