class AutoPilotLog:
    def __init__(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list):
        self.current_load = current_load
        self.feed_multiplier = feed_multiplier
        self.time = time
        self.raw_loads = raw_loads
        self.average_loads = average_loads
        self.raw_multiplier = raw_multiplier
        self.adjustment_list = str(adjustment_list).replace('[', '').replace(']', '')


import datetime
from gsheet_helper import *
from random import uniform, randint


def get_safe(listt, index):
    try:
        return listt[index]
    except IndexError:
        return 'n/a'


class AutoPilotLogger:
    logs = []

    def __init__(self, spindle_v_main, spindle_target_watts, bias, m_coefficient, c_coefficient, increase_cap,
                 decrease_cap, job_name, serial_number, delay_between_feed_adjustments, outlier_amount):
        self.spindle_v_main = spindle_v_main
        self.spindle_target_watts = spindle_target_watts
        self.bias = bias
        self.m_coefficient = m_coefficient
        self.c_coefficient = c_coefficient
        self.increase_cap = increase_cap
        self.decrease_cap = decrease_cap
        self.job_name = job_name
        self.serial_number = serial_number
        self.delay_between_feed_adjustments = delay_between_feed_adjustments
        self.outlier_amount = outlier_amount

    def add_log(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list):
        self.logs.append(AutoPilotLog(current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier,
                                      adjustment_list))

    def get_data_for_sheet(self):
        data = [['Time', 'Raw Load 1', 'Raw Load 2', 'Raw Load 3', 'Raw Load 4', 'Raw Load 5', 'Average Load 1',
                 'Average Load 2', 'Average Load 3', 'Average Load 4', 'Average Load 5', 'Average Load',
                 'Raw Multiplier', 'Capped Multiplier', 'Adjustment List']]
        for log in self.logs:
            data.append([log.time, get_safe(log.raw_loads, 0),
                         get_safe(log.raw_loads, 1), get_safe(log.raw_loads, 2), get_safe(log.raw_loads, 3),
                         get_safe(log.raw_loads, 4), get_safe(log.average_loads, 0),
                         get_safe(log.average_loads, 1), get_safe(log.average_loads, 2),
                         get_safe(log.average_loads, 3), get_safe(log.average_loads, 4),
                         log.current_load, log.raw_multiplier, log.feed_multiplier, log.adjustment_list])
        return data

    def export_to_gsheet(self):
        sheet_name = self.job_name + '-YS' + str(self.serial_number)

        spreadsheet_id = create(sheet_name)

        data = self.get_data_for_sheet()

        add_sheet(spreadsheet_id, 'Feed Factor Profile')

        add_img_to_sheet(spreadsheet_id, "https://lh3.googleusercontent.com/u/0/drive-viewer/AFDK6gOfn33pDikRiDOrGcEet7A55OKNtNNgb4Z-mqqaU734XAXX2s29RxYRhG1e91j_tCSoz_YKICgAs3bAdOCI3UZIiad-bg=w2556-h1614")

        add_sheet(spreadsheet_id, 'Data')

        rename_sheet(spreadsheet_id, 'Sheet1', 'Parameters')

        write_data_to_sheet(spreadsheet_id, data)

        write_other_data_to_sheet(spreadsheet_id, self.spindle_v_main, self.spindle_target_watts, self.bias,
                                  self.m_coefficient, self.c_coefficient, self.increase_cap, self.decrease_cap)

        create_chart(spreadsheet_id)

        create_time_chart(spreadsheet_id)

        rename_sheet(spreadsheet_id, 'Chart1', 'Spindle Load vs Feed Multiplier')

        rename_sheet(spreadsheet_id, 'Chart2', 'Spindle Load vs Time')

        move_spreadsheet(spreadsheet_id, "1FwSQqN98_T39rtHd522KlLOTwxfcygsV")

        url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet_id

        print('Spreadsheet: ' + url)


def get_random_time():
    hours = randint(1, 23)
    minutes = randint(1, 59)
    seconds = randint(1, 59)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


if __name__ == '__main__':
    logger = AutoPilotLogger(0, 0, 0, 0, 0, 0, 0, "job.gcode", "ys61234")

    time = datetime.datetime.now()

    for i in range(2000):
        log_time = time + datetime.timedelta(seconds=i)
        logger.add_log(i, uniform(-4000, 2000) / 100, log_time.strftime('%H:%M:%S'), [], [], 0, [])

    logger.export_to_gsheet()