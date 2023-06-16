import sys
import logging
import json

from confluent_kafka import Consumer, KafkaException, KafkaError

from ner_analyzer import NerParser
from ner_producer import NerProducer


logger = logging.getLogger('consumer')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


send_to_topic = "ner-topic"


def msg_process(msg, analyzer, producer):
    msg_processed = analyzer.find(str(msg.value()))  # ["word 1 qwert", "asdasdf"] or []
    producer.send(send_to_topic, msg_processed)


def basic_consume_loop(consumer, topics):
    try:
        analyser = NerParser()
        producer = NerProducer()

        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg, analyser, producer)
    finally:
        consumer.close()


def shutdown():
    running = False


if __name__ == '__main__':
    conf = {'bootstrap.servers': 'kafka-1:9092',
            'group.id': "ner_group",
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'}

    consumer = Consumer(conf)
    running = True
    basic_consume_loop(consumer, ["tweets-topic"])
    shutdown()
