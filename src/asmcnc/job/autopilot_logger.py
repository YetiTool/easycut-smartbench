class AutoPilotLog:
    def __init__(self, current_load, feed_multiplier, time):
        self.current_load = current_load
        self.feed_multiplier = feed_multiplier
        self.time = time


from datetime import datetime
from gsheet_helper import create, write_other_data_to_sheet, write_data_to_sheet, create_chart, create_time_chart
from random import uniform


class AutoPilotLogger:
    logs = []

    def __init__(self, spindle_v_main, spindle_target_watts, bias, m_coefficient, c_coefficient, increase_cap,
                 decrease_cap):
        self.spindle_v_main = spindle_v_main
        self.spindle_target_watts = spindle_target_watts
        self.bias = bias
        self.m_coefficient = m_coefficient
        self.c_coefficient = c_coefficient
        self.increase_cap = increase_cap
        self.decrease_cap = decrease_cap

    def add_log(self, current_load, feed_multiplier, time):
        self.logs.append(AutoPilotLog(current_load, feed_multiplier, time))

    def get_data_for_sheet(self):
        data = [['Feed Multiplier', 'Current Load', 'Time']]
        for log in self.logs:
            data.append([log.current_load, log.feed_multiplier, log.time])
        return data

    def export_to_gsheet(self):
        sheet_name = 'Autopilot Logs - ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        spreadsheet_id = create(sheet_name)

        data = self.get_data_for_sheet()

        write_data_to_sheet(spreadsheet_id, data)

        write_other_data_to_sheet(spreadsheet_id, self.spindle_v_main, self.spindle_target_watts, self.bias,
                                  self.m_coefficient, self.c_coefficient, self.increase_cap, self.decrease_cap)

        create_chart(spreadsheet_id)

        create_time_chart(spreadsheet_id)

        url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet_id

        print('Spreadsheet: ' + url)


if __name__ == '__main__':
    logger = AutoPilotLogger(0, 0, 0, 0, 0, 0, 0)

    for i in range(2000):
        logger.add_log(uniform(-4000, 2000) / 100, i, datetime.now().strftime('%H:%M:%S'))

    logger.export_to_gsheet()