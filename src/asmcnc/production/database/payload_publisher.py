import pika
import random
import datetime
import json
import uuid
from asmcnc.production.database import credentials as creds

QUEUE = 'calibration_data'


def get_full_payload(data, table):
    return {
        "Table": table,
        "Statuses": data
    }


class Publisher(object):
    def __init__(self):
        self.create_channel_connection()

    def create_channel_connection(self):
        credentials = pika.PlainCredentials(
            username='calibration',
            password=creds.password
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='51.68.204.96',
                credentials=credentials
            )
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(
            queue=QUEUE,
            durable=True
        )

        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True
        )

    def _on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = body

    def _publish(self, data):
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        data = json.dumps(data)

        self.channel.basic_publish(
            exchange='',
            routing_key=QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id
            ),
            body=data
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response

    def publish(self, data, table):
        self._publish(get_full_payload(data, table))

def gfloat(a, b):
    return random.uniform(a, b)


def gint(a, b):
    return random.randint(a, b)


def generate_status():
    return {
        "Id": "",
        "FTID": gint(10000, 60000),
        "XCoordinate": gfloat(0, 3000), "YCoordinate": gfloat(0, 3000), "ZCoordinate": gfloat(0, 3000),
        "XDirection": gint(0, 1), "YDirection": gint(0, 1), "ZDirection": gint(0, 1),
        "XSG": gint(0, 250), "YSG": gint(0, 250), "Y1SG": gint(0, 250), "Y2SG": gint(0, 250), "ZSG": gint(0, 250),
        "TMCTemperature": gint(30, 80), "PCBTemperature": gint(30, 80), "MOTTemperature": gint(30, 80),
        "Timestamp": datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        "Feedrate": gint(0, 1500),
        "XWeight": gint(0, 10), "YWeight": gint(0, 10), "ZWeight": gint(0, 10)
    }

def generate_payload():
    return [generate_status() for _ in range(0, 200000)]

#
# if __name__ == '__main__':
#     publisher = Publisher()
#
#     payload = get_full_payload("FinalTestStatuses")
#
#     response = publisher.publish(payload)
#
#     if len(response) < 100:
#         print(response)
