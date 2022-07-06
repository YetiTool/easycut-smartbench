import pika
import json
import pandas
import os
import pyodbc
from time import sleep
import uuid
import threading

QUEUE = 'calibration_data'
CONN_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1435;DATABASE=CalibrationTest;UID=Calibration;PWD=K+rJ-6*u6VHPB*Md;'

class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost'
            )
        )

        self.received = False
        self.inserted = False

        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue=QUEUE,
            durable=True
        )

        self._connect_to_db()

    def _connect_to_db(self):
        self.db_connection = pyodbc.connect(CONN_STRING)

    def _reply(self, ch, properties):
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            ),
            body='Done'
        )

    def insert_csv(self, full_path, table):
        query = f"""
            BULK INSERT {table}
                FROM '{full_path}'
                WITH
                (
                    FIRSTROW = 2,
                    FIELDTERMINATOR = ','
                )
                """

        self.db_connection.execute(query)
        self.db_connection.commit()

        print('Inserted')

    def wait_till_exported(self, full_path, table):
        while not os.path.exists(full_path):
            sleep(0.5)

        self.insert_csv(full_path, table)

    def sort_jobj(self, obj):
        return {
            "Id": "",
            "FTID": obj["FTID"],
            "XCoordinate": obj["XCoordinate"], "YCoordinate": obj["YCoordinate"], "ZCoordinate": obj["ZCoordinate"],
            "XDirection": obj["XDirection"], "YDirection": obj["YDirection"], "ZDirection": obj["ZDirection"],
            "XSG": obj["XSG"], "YSG": obj["YSG"], "Y1SG": obj["Y1SG"], "Y2SG": obj["Y2SG"], "ZSG": obj["ZSG"],
            "TMCTemperature": obj["TMCTemperature"], "PCBTemperature": obj["PCBTemperature"], "MOTTemperature": obj["MOTTemperature"],
            "Timestamp": obj["Timestamp"],
            "Feedrate": obj["Feedrate"],
            "XWeight": obj["XWeight"], "YWeight": obj["YWeight"], "ZWeight": obj["ZWeight"]
        }

    def sort_payload(self, payload):
        return [self.sort_jobj(obj) for obj in payload]

    def _on_message_recv(self, ch, method, properties, body):
        if body is None:
            return

        print('Received message')

        data = json.loads(body)
        data_table = data["Table"]
        data_statuses = self.sort_payload(data["Statuses"])
        data_statuses_count = len(data_statuses)

        print(data_statuses)

        print(f'Table: {data_table}, Statuses: {data_statuses_count}')

        df = pandas.read_json(json.dumps(data_statuses))

        file_name = f"{uuid.uuid4()}.csv"  # way of handling duplicates # way of recognising machines
        full_path = f"C:\\CalibrationReceiver\\CSVS\\{file_name}"

        df.to_csv(full_path, encoding='utf-8', index=False)

        threading.Thread(target=self.wait_till_exported(full_path, data_table)).start()

        self._reply(ch, properties)

    def start_consuming(self):
        self.channel.basic_consume(
            queue=QUEUE,
            on_message_callback=self._on_message_recv
        )

        self.channel.start_consuming()

if __name__ == '__main__':
    consumer = Consumer()

    print('Waiting for messages')

    consumer.start_consuming()
