import sys
from confluent_kafka import Producer
import socket
import pandas as pd
import concurrent.futures


def send(producer, message):
    producer.produce('detect_lang', value=message)
    producer.flush()


def main(file_name):
    try:
        conf = {
            'bootstrap.servers': "kafka-1:9092",
            'client.id': socket.gethostname()
        }

        producer = Producer(conf)

        df = pd.read_csv(f'./src/{file_name}')

        messages = list(df['text'])

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            futures = []
            for msg in messages:
                futures.append(executor.submit(send, producer=producer, message=msg))
            for future in concurrent.futures.as_completed(futures):
                future.result()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    args = sys.argv
    main(args[1])
