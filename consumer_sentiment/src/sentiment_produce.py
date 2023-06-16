from confluent_kafka import Producer
import socket

class SentimentProducer:
    def __init__(self) -> None:
        self._producer = self._init_producer() 

    def _init_producer(self):
        conf = {
            'bootstrap.servers': "kafka-1:9092",
            'client.id': socket.gethostname()
        }

        producer = Producer(conf)

        return producer

    def send(self, topic, message):
        self._producer.produce(topic, value=message)
        self._producer.flush()
