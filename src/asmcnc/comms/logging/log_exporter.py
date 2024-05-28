from datetime import datetime
import os
import sys
from asmcnc.comms.logging_system.logging_system import Logger

WORKING_DIR = "A:\\Logs\\"
export_logs_folder = "/home/pi/exported_logs"
ftp_server = None
ftp_username = None
ftp_password = None
creds_imported = False
try:
    import paramiko
except (ImportWarning, ImportError):
    Logger.exception("Unable to import paramiko")


def try_import_creds():
    global ftp_server, ftp_username, ftp_password, creds_imported
    try:
        from asmcnc.production.database import credentials as creds

        ftp_server = creds.ftp_server
        ftp_username = creds.ftp_username
        ftp_password = creds.ftp_password
        creds_imported = True
    except:
        Logger.exception("Log exporter not available")
        try:
            from ...production.database import credentials as creds

            Logger.debug("Imported creds from dev path")
        except Exception:
            Logger.exception("Creds not available from dev path")


def create_log_folder():
    os.system("rm -r " + export_logs_folder)
    if not os.path.exists(export_logs_folder) or not os.path.isdir(export_logs_folder):
        os.mkdir(export_logs_folder)


def create_and_send_logs(serial_number):
    create_log_folder()
    log_file_path = generate_logs(serial_number)
    send_logs(log_file_path)


def create_trim_and_send_logs(serial_number, x_lines):
    create_log_folder()
    log_file_path = generate_logs(serial_number)
    trim_logs(export_logs_folder + "/" + log_file_path, x_lines)
    send_logs(log_file_path)


def generate_logs(serial_number):
    create_log_folder()
    str_current_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    log_name = (
        "smartbench-exported-logs-"
        + str_current_time
        + "-"
        + str(serial_number)
        + ".txt"
    )
    full_path = export_logs_folder + "/" + log_name
    command = "journalctl > " + full_path
    sys.stdout.flush()
    os.system(command)
    return log_name


def trim_logs(log_file_path, x_lines):
    with open(log_file_path, "r+") as untrimmed_file:
        lines = untrimmed_file.readlines()
        line_count = len(lines)
    if x_lines > line_count:
        return
    with open(log_file_path, "w+") as trimmed_file:
        lines_to_remove = line_count - x_lines
        new_lines = lines[lines_to_remove:]
        trimmed_file.writelines(new_lines)
        trimmed_file.close()


def send_logs(log_file_path):
    if not creds_imported:
        try_import_creds()
    Logger.info("Sending logs to server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    Logger.debug("Connecting to: " + ftp_server)
    ssh.connect(ftp_server, username=ftp_username, password=ftp_password)
    Logger.info("Connected to: " + ftp_server)
    sftp = ssh.open_sftp()
    file_name = log_file_path.split("/")[-1]
    Logger.debug("Transferring file: " + file_name)
    sftp.put(export_logs_folder + "/" + log_file_path, WORKING_DIR + file_name)
    Logger.info("Done sending logs to server")


if __name__ == "__main__":
    Logger.info("Testing basic log send")
    create_trim_and_send_logs("123456", 100)
