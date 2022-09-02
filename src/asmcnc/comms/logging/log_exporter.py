from datetime import datetime
import os
from asmcnc.production.database import credentials as creds
import paramiko
import sys

WORKING_DIR = 'C:\\SBLogs\\'

export_logs_folder = '/home/pi/exported_logs'

def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))

def create_log_folder():
    # remove all logs when creating new one
    os.system("rm -r " + export_logs_folder)

    if not os.path.exists(export_logs_folder) or not os.path.isdir(export_logs_folder):
        os.mkdir(export_logs_folder)


def create_and_send_logs(serial_number):
    create_log_folder()

    log_file_path = generate_logs(serial_number)
    send_logs(log_file_path)


def generate_logs(serial_number):
    create_log_folder()

    str_current_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    log_name = "smartbench-exported-logs-" + str_current_time + "-" + str(serial_number) + ".txt"
    full_path = export_logs_folder + '/' + log_name

    command = "journalctl > " + full_path
    sys.stdout.flush()
    os.system(command)

    return log_name


def trim_logs(log_file_path, x_lines):
    with open(log_file_path, 'r+') as untrimmed_file:
        lines = untrimmed_file.readlines()
        line_count = len(lines)

    with open(log_file_path, 'w+') as trimmed_file:
        lines_to_remove = line_count - x_lines
        new_lines = lines[lines_to_remove:]

        trimmed_file.writelines(new_lines)
        trimmed_file.close()


def send_logs(log_file_path):
    log("Sending logs to server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(creds.ftp_server, username=creds.ftp_username, password=creds.ftp_password)
    sftp = ssh.open_sftp()

    file_name = log_file_path.split('/')[-1]
    sftp.put(export_logs_folder + "/" + log_file_path, WORKING_DIR + file_name)
    log("Done sending logs to server")
