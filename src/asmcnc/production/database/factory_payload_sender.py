import os
import csv
import uuid

CSV_PATH = 'asmcnc/production/database/csvs/'
WORKING_DIR = 'A:\\factory_data\\data\\new\\'


def get_unique_file_name(machine_serial, table, stage):
    return str(machine_serial) + '-' + str(table) + '-' + str(stage) + '-' + str(uuid.uuid4()) + '.csv'


def get_csv(json, machine_serial, table, stage=None, csv_path=CSV_PATH):
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)

    file_path = csv_path + get_unique_file_name(machine_serial, table, stage)

    keys = json[0].keys()

    with open(file_path, 'w') as data_file:
        dict_writer = csv.DictWriter(data_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(json)

    return file_path


def send_csv_to_ftp(file_path, ftp_server=None, ftp_username=None, ftp_password=None):
    try:
        if "credentials.py" in os.listdir("/media/usb/"):
            os.system("cp /media/usb/credentials.py ./asmcnc/production/database/credentials.py")
    except OSError:
        print('credentials.py not found on USB')
        return False

    if ftp_server is None or ftp_username is None or ftp_password is None:
        try:
            from asmcnc.production.database.credentials import ftp_server, ftp_username, ftp_password
        except ImportError:
            print('credentials.py not found locally')
            return False

    try:
        import paramiko
    except ImportError:
        print('paramiko not installed')
        return False

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ftp_server, username=ftp_username, password=ftp_password)
        sftp = ssh.open_sftp()

        file_name = file_path.split('/')[-1]
        sftp.put(file_path, WORKING_DIR + file_name)
        sftp.close()
        ssh.close()
        return True
    except Exception as e:
        print(e)

    return False
