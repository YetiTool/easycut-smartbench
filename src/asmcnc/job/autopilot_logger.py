import datetime
from gsheet_helper import *
from random import uniform, randint


class AutoPilotLog:
    def __init__(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list,
                 feed_override_percentage, moving_in_z, sg_x_motor_axis, sg_y_axis, sg_z_motor_axis, sg_x1_motor,
                 sg_x2_motor,
                 sg_y1_motor, sg_y2_motor):
        self.current_load = current_load
        self.feed_multiplier = feed_multiplier
        self.time = time
        self.raw_loads = raw_loads
        self.average_loads = average_loads
        self.raw_multiplier = raw_multiplier
        self.adjustment_list = str(adjustment_list).replace('[', '').replace(']', '')
        self.feed_override_percentage = feed_override_percentage
        self.moving_in_z = moving_in_z
        self.sg_x_motor_axis = sg_x_motor_axis if sg_x_motor_axis > 0 else 0
        self.sg_y_axis = sg_y_axis if sg_y_axis > 0 else 0
        self.sg_z_motor_axis = sg_z_motor_axis if sg_z_motor_axis > 0 else 0
        self.sg_x1_motor = sg_x1_motor if sg_x1_motor > 0 else 0
        self.sg_x2_motor = sg_x2_motor if sg_x2_motor > 0 else 0
        self.sg_y1_motor = sg_y1_motor if sg_y1_motor > 0 else 0
        self.sg_y2_motor = sg_y2_motor if sg_y2_motor > 0 else 0


def get_safe(listt, index):
    try:
        return listt[index]
    except IndexError:
        return 'n/a'


class AutoPilotLogger:
    logs = []
    exported = False

    def __init__(self, spindle_v_main, spindle_target_watts, increase_bias, decrease_bias, m_coefficient, c_coefficient,
                 increase_cap,
                 decrease_cap, job_name, serial_number, delay_between_feed_adjustments, outlier_amount,
                 cap_for_feed_increase_during_z_movement):
        self.spindle_v_main = spindle_v_main
        self.spindle_target_watts = spindle_target_watts
        self.increase_bias = increase_bias
        self.decrease_bias = decrease_bias
        self.m_coefficient = m_coefficient
        self.c_coefficient = c_coefficient
        self.increase_cap = increase_cap
        self.decrease_cap = decrease_cap
        self.job_name = job_name
        self.serial_number = serial_number
        self.delay_between_feed_adjustments = delay_between_feed_adjustments
        self.outlier_amount = outlier_amount
        self.cap_for_feed_increase_during_z_movement = cap_for_feed_increase_during_z_movement

    def add_log(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list,
                feed_override_percentage, moving_in_z, sg_x_motor_axis, sg_y_axis, sg_z_motor_axis, sg_x1_motor,
                sg_x2_motor, sg_y1_motor, sg_y2_motor):
        self.logs.append(AutoPilotLog(current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier,
                                      adjustment_list, feed_override_percentage, moving_in_z, sg_x_motor_axis,
                                      sg_y_axis,
                                      sg_z_motor_axis, sg_x1_motor, sg_x2_motor, sg_y1_motor, sg_y2_motor))

    def get_data_for_sheet(self):
        data = [['Time', 'Raw Load 1', 'Raw Load 2', 'Raw Load 3', 'Raw Load 4', 'Raw Load 5', 'Average Load 1',
                 'Average Load 2', 'Average Load 3', 'Average Load 4', 'Average Load 5', 'Average Load',
                 'Raw Multiplier', 'Capped Multiplier', 'Adjustment List', "Moving in Z", "Feed Override % Status",
                 "X Motor Axis", "Y Motor Axis", "Z Motor Axis", "X1 Motor", "X2 Motor", "Y1 Motor", "Y2 Motor"]]
        for log in self.logs:
            data.append([log.time, get_safe(log.raw_loads, 0),
                         get_safe(log.raw_loads, 1), get_safe(log.raw_loads, 2), get_safe(log.raw_loads, 3),
                         get_safe(log.raw_loads, 4), get_safe(log.average_loads, 0),
                         get_safe(log.average_loads, 1), get_safe(log.average_loads, 2),
                         get_safe(log.average_loads, 3), get_safe(log.average_loads, 4),
                         log.current_load, log.raw_multiplier, log.feed_multiplier, log.adjustment_list,
                         log.moving_in_z, log.feed_override_percentage, log.sg_x_motor_axis, log.sg_y_axis,
                         log.sg_z_motor_axis, log.sg_x1_motor, log.sg_x2_motor, log.sg_y1_motor, log.sg_y2_motor])
        return data

    def get_feed_multiplier(self, current_power):
        multiplier = (float(self.decrease_bias) if current_power > self.spindle_target_watts else 1) * (
                float(self.spindle_target_watts) - float(current_power)) / float(self.spindle_target_watts) \
                     * float(self.m_coefficient) * float(self.c_coefficient)

        if multiplier > self.increase_cap:
            multiplier = self.increase_cap

        if multiplier < self.decrease_cap:
            multiplier = self.decrease_cap

        return multiplier

    def get_sweep(self):
        sweep = [["Spindle Load", "Feed Multiplier"]]
        for power in range(0, 1750):
            sweep.append([power, self.get_feed_multiplier(power)])
        return sweep

    def export_to_gsheet(self):
        if self.exported:
            return

        self.exported = True

        export_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet_name = export_time + '-' + self.job_name + '-YS' + str(self.serial_number)

        spreadsheet_id = create(sheet_name)

        data = self.get_data_for_sheet()

        add_sheet(spreadsheet_id, 'Data')

        rename_sheet(spreadsheet_id, 'Sheet1', 'Parameters')

        add_feed_multiplier_sweep(spreadsheet_id, self.get_sweep())

        write_data_to_sheet(spreadsheet_id, data)

        write_other_data_to_sheet(spreadsheet_id, self.spindle_v_main, self.spindle_target_watts, self.increase_bias,
                                  self.decrease_bias, self.m_coefficient, self.c_coefficient, self.increase_cap,
                                  self.decrease_cap, self.delay_between_feed_adjustments, self.outlier_amount,
                                  self.cap_for_feed_increase_during_z_movement)

        create_chart(spreadsheet_id)

        create_time_chart(spreadsheet_id)

        rename_sheet(spreadsheet_id, 'Chart1', 'Spindle Load vs Feed Multiplier')

        rename_sheet(spreadsheet_id, 'Chart2', 'Spindle Load vs Time')

        move_spreadsheet(spreadsheet_id, "1FwSQqN98_T39rtHd522KlLOTwxfcygsV")

        url = 'https://docs.google.com/spreadsheets/d/' + spreadsheet_id

        print('Spreadsheet: ' + url)

    def reset(self):
        self.logs = []
        self.exported = False


def get_random_time():
    hours = randint(1, 23)
    minutes = randint(1, 59)
    seconds = randint(1, 59)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


if __name__ == '__main__':
    logger = AutoPilotLogger(230, 875, 2, 1, 35, 20, -40, "job.gcode", "ys61234", 0.5, 100, 0, 0)

    time = datetime.datetime.now()

    for i in range(1750):
        log_time = time + datetime.timedelta(seconds=i)

        raw_loads = [uniform(0, 1000) for i in range(5)]

        average = sum(raw_loads) / len(raw_loads)

        logger.add_log(average, logger.get_feed_multiplier(average), log_time.strftime('%H:%M:%S'), raw_loads, [], 0,
                       [], 0, False, 0, 0, 0, 0, 0, 0, 0)

    logger.export_to_gsheet()

    logger.reset()

    logger.export_to_gsheet()

    difference = datetime.datetime.now() - time

    print(difference)
