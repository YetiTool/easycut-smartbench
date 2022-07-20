import pika
import uuid
import csv
import json
import paramiko

CSV_PATH = '/home/pi/easycut-smartbench/src/asmcnc/production/database/csvs/'
QUEUE = 'calibration_data'
WORKING_DIR = 'C:\\CalibrationReceiver\\CSVS\\'


def get_unique_file_name(machine_serial):
    return machine_serial + str(uuid.uuid4()) + '.csv'


def json_to_csv(data, machine_serial):
    file_path = CSV_PATH + get_unique_file_name(machine_serial)

    keys = data[0].keys()

    with open(file_path, 'w') as data_file:
        dict_writer = csv.DictWriter(data_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    return file_path


class DataPublisher(object):
    def __init__(self, machine_serial):
        self.import_credentials()

        print(credentials.password)

        self.machine_serial = machine_serial

        pika_credentials = pika.PlainCredentials(
            username='calibration',
            password=credentials.password
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='51.68.204.96',
                credentials=pika_credentials
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

    def import_credentials(self):
        from asmcnc.production.database import credentials

    def send_file_paramiko_sftp(self, file_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(credentials.ftp_server, username=credentials.ftp_username, password=credentials.ftp_password)
        sftp = ssh.open_sftp()

        file_name = file_path.split('/')[-1]
        sftp.put(file_path, WORKING_DIR + file_name)

    def publish(self, data):
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id
            ),
            body=json.dumps(data)
        )

        print('Sent message')

        while self.response is None:
            self.connection.process_data_events()

        return self.response

    def _on_response(self, ch, method, props, body):
        if body['Inserted']:
            print('Inserted successfully')
        else:
            print('Failed to insert')

    def run_data_send(self, statuses, table):
        print(credentials.password)
        csv_name = json_to_csv(statuses, self.machine_serial)
        self.send_file_paramiko_sftp(csv_name)

        raw_file_name = csv_name.split('/')[-1]

        payload = {
            'MachineSerial': self.machine_serial,
            'FileName': raw_file_name,
            'Table': table
        }

        return self.publish(payload)


# import datetime
# import random
#
#
# def gfloat(a, b):
#     return random.uniform(a, b)
#
#
# def gint(a, b):
#     return random.randint(a, b)
#
#
# def generate_status():
#     return {
#         "Id": "",
#         "FTID": gint(1000, 6000),
#         "XCoordinate": gfloat(0, 3000), "YCoordinate": gfloat(0, 3000), "ZCoordinate": gfloat(0, 3000),
#         "XDirection": gint(0, 1), "YDirection": gint(0, 1), "ZDirection": gint(0, 1),
#         "XSG": gint(0, 250), "YSG": gint(0, 250), "Y1SG": gint(0, 250), "Y2SG": gint(0, 250), "ZSG": gint(0, 250),
#         "TMCTemperature": gint(30, 80), "PCBTemperature": gint(30, 80), "MOTTemperature": gint(30, 80),
#         "Timestamp": datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
#         "Feedrate": gint(0, 1500),
#         "XWeight": gint(0, 10), "YWeight": gint(0, 10), "ZWeight": gint(0, 10)
#     }
#
#
# def generate_payload():
#     return [generate_status() for _ in range(0, 10)]
#
#
# if __name__ == '__main__':
#     serial = 'YS6139'
#
#     publisher = DataPublisher(serial)
#
#     publisher.run_data_send(generate_payload(), "FinalTestStatuses")
