from datetime import datetime
import os


def generate_logs():
    str_current_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    log_name = "easycut-exported-logs-" + str_current_time + ".txt"
    command = "journalctl > " + log_name

    os.system(command)

    return log_name


def trim_logs(log_file_path, x_lines):
    with open(log_file_path, 'r') as untrimmed_file:
        lines = untrimmed_file.readlines()

        lines_to_remove = len(lines) - x_lines

        new_lines = lines[lines_to_remove:]

        untrimmed_file.truncate()

        untrimmed_file.writelines(new_lines)


def send_logs(log_file_path):
    pass
