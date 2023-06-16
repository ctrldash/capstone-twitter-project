import json 

from confluent_kafka import SerializingProducer
import socket



def json_serializer(msg, s_obj):
    return json.dumps(msg).encode('utf-8')


class NerProducer:
    def __init__(self) -> None:
        self._producer = self._init_producer() 

    def _init_producer(self):
        conf = {
            'bootstrap.servers': "kafka-1:9092",
            'client.id': socket.gethostname(),
            'value.serializer': json_serializer
        }

        producer = SerializingProducer(conf)

        return producer

    def send(self, topic, message):
        self._producer.produce(topic, value=message)
        self._producer.flush()
