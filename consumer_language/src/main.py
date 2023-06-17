import sys
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError
from language_analysator import LanguageAnalysator
from language_produce import LanguageProducer


logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


def msg_process(msg, analyzer, producer):
    msg_language = analyzer.run(str(msg.value()))

    producer.send("languages-topic", msg_language)


def basic_consume_loop(consumer, topics):
    try:
        language_analysator = LanguageAnalysator()
        language_producer = LanguageProducer()

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
                msg_process(msg, language_analysator, language_producer)
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
    basic_consume_loop(consumer, ["tweets-topic"])
    shutdown()
