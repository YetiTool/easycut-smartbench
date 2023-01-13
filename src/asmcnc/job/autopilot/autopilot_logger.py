import datetime
from random import uniform, randint
import autopilot_exporter


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
        self.sg_x_motor_axis = sg_x_motor_axis if sg_x_motor_axis > 0 else ''
        self.sg_y_axis = sg_y_axis if sg_y_axis > 0 else ''
        self.sg_z_motor_axis = sg_z_motor_axis if sg_z_motor_axis > 0 else ''
        self.sg_x1_motor = sg_x1_motor if sg_x1_motor > 0 else ''
        self.sg_x2_motor = sg_x2_motor if sg_x2_motor > 0 else ''
        self.sg_y1_motor = sg_y1_motor if sg_y1_motor > 0 else ''
        self.sg_y2_motor = sg_y2_motor if sg_y2_motor > 0 else ''


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
                 cap_for_feed_increase_during_z_movement, autopilot_instance):
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
        self.autopilot_instance = autopilot_instance

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
            multiplier = self.get_feed_multiplier(power)
            sweep.append([power, multiplier])
        return sweep

    def get_parameter_format(self):
        return [
            ["Spindle Mains Voltage", self.spindle_v_main],
            ["Spindle Target Watts", self.spindle_target_watts],
            ["Bias for Feed Increase", self.increase_bias],
            ["Bias for Feed Decrease", self.decrease_bias],
            ["M Coefficient", self.m_coefficient],
            ["C Coefficient", self.c_coefficient],
            ["Cap for Feed Increase", self.increase_cap],
            ["Cap for Feed Decrease", self.decrease_cap],
            ["Delay Between Feed Adjustments", self.delay_between_feed_adjustments],
            ["Outlier Amount", self.outlier_amount],
            ["Cap for Feed-Up Change When Moving in Z", self.cap_for_feed_increase_during_z_movement]
        ]

    def export_to_gsheet(self):
        export_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = export_time + '-' + self.job_name + '-YS' + str(self.serial_number)
        autopilot_exporter.run(title, self)
        self.reset()
        self.exported = True

    def reset(self):
        del self.logs
        self.logs = []
        self.exported = False


def get_random_time():
    hours = randint(1, 23)
    minutes = randint(1, 59)
    seconds = randint(1, 59)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


if __name__ == '__main__':
    logger = AutoPilotLogger(230, 875, 10, 10, 10, 10, 10, 10, "job.gcode", "123", 10, 10, 10, None)

    time = datetime.datetime.now()

    for i in range(5000):
        log_time = time + datetime.timedelta(seconds=i)

        raw_loads = [uniform(0, 1000) for i in range(5)]

        average = sum(raw_loads) / len(raw_loads)

        logger.add_log(average, logger.get_feed_multiplier(average), log_time.strftime('%H:%M:%S'), raw_loads, [], 0,
                       [], 0, False, 1, 1, 1, 1, 1, 1, 1)

    logger.export_to_gsheet(None)

    difference = datetime.datetime.now() - time

    print(difference)
