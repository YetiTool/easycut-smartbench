import datetime
from random import randint
import json
import yetipilot_exporter


class AutoPilotLog:
    def __init__(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list,
                 feed_override_percentage, moving_in_z, sg_x_motor_axis, sg_y_axis, sg_z_motor_axis, sg_x1_motor,
                 sg_x2_motor,
                 sg_y1_motor, sg_y2_motor, target_load, raw_spindle_load, spindle_voltage, feed_rate, constant_speed,
                 line_number, gcode_feed, target_feed, g0_move, allow_feedup, target_spindle_speed, spindle_override_percentage,
                 spindle_rpm, gcode):
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
        self.target_load = target_load
        self.raw_spindle_load = raw_spindle_load
        self.spindle_voltage = spindle_voltage
        self.feed_rate = feed_rate
        self.line_number = line_number
        self.gcode_feed = gcode_feed
        self.target_feed = target_feed
        self.constant_speed = constant_speed
        self.g0_move = g0_move
        self.allow_feedup = allow_feedup
        self.target_spindle_speed = target_spindle_speed
        self.spindle_override_percentage = spindle_override_percentage
        self.spindle_rpm = spindle_rpm
        self.gcode = gcode


def get_safe(listt, index):
    try:
        return listt[index]
    except IndexError:
        return 'n/a'


def limit(value):
    try:
        return round(value, 2)
    except:
        return value


class AutoPilotLogger:
    logs = []
    exported = False

    def __init__(self, spindle_v_main, spindle_target_watts, increase_bias, decrease_bias, m_coefficient, c_coefficient,
                 increase_cap,
                 decrease_cap, job_name, serial_number, delay_between_feed_adjustments, outlier_amount,
                 cap_for_feed_increase_during_z_movement, autopilot_instance, job_start_time):
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
        self.job_start_time = job_start_time

    def add_log(self, current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier, adjustment_list,
                feed_override_percentage, moving_in_z, sg_x_motor_axis, sg_y_axis, sg_z_motor_axis, sg_x1_motor,
                sg_x2_motor, sg_y1_motor, sg_y2_motor, target_load, raw_spindle_load, spindle_voltage, feed_rate,
                constant_speed, line_number, gcode_feed, target_feed, g0_move, allow_feedup, target_spindle_speed,
                spindle_override_percentage, spindle_rpm, gcode):
        self.logs.append(AutoPilotLog(current_load, feed_multiplier, time, raw_loads, average_loads, raw_multiplier,
                                      adjustment_list, feed_override_percentage, moving_in_z, sg_x_motor_axis,
                                      sg_y_axis, sg_z_motor_axis, sg_x1_motor, sg_x2_motor, sg_y1_motor, sg_y2_motor,
                                      target_load, raw_spindle_load, spindle_voltage, feed_rate, constant_speed,
                                      line_number, gcode_feed, target_feed, g0_move, allow_feedup, target_spindle_speed,
                                      spindle_override_percentage, spindle_rpm, gcode))

    def get_data_for_sheet(self):
        data = [['Time', 'Raw Load 1', 'Raw Load 2', 'Raw Load 3', 'Raw Load 4', 'Raw Load 5', 'Average Load 1',
                 'Average Load 2', 'Average Load 3', 'Average Load 4', 'Average Load 5', 'Calculated Load',
                 "Target Load",
                 'Raw Multiplier', 'Capped Multiplier', 'Adjustment List', "Moving in Z", "Feed Override % Status",
                 "X Motor Axis", "Y Motor Axis", "Z Motor Axis", "X1 Motor", "X2 Motor", "Y1 Motor", "Y2 Motor",
                 "Raw Spindle Load", "Spindle Voltage", "Actual Feed", "Line #", "GCode Feed", "Actual Feed Override %",
                 "Target Feed", "Constant Feed"]]
        for log in self.logs:
            data.append([log.time, get_safe(log.raw_loads, 0),
                         get_safe(log.raw_loads, 1), get_safe(log.raw_loads, 2), get_safe(log.raw_loads, 3),
                         get_safe(log.raw_loads, 4), get_safe(log.average_loads, 0),
                         get_safe(log.average_loads, 1), get_safe(log.average_loads, 2),
                         get_safe(log.average_loads, 3), get_safe(log.average_loads, 4),
                         log.current_load, log.target_load, log.raw_multiplier, log.feed_multiplier,
                         log.adjustment_list,
                         log.moving_in_z, log.feed_override_percentage, log.sg_x_motor_axis, log.sg_y_axis,
                         log.sg_z_motor_axis, log.sg_x1_motor, log.sg_x2_motor, log.sg_y1_motor, log.sg_y2_motor,
                         log.raw_spindle_load, log.spindle_voltage, int(log.feed_rate), log.line_number,
                         log.gcode_feed, log.feed_override_percentage, log.target_feed,
                         log.constant_speed])
        return data

    def get_data_for_test_data_sheet(self):
        data = [["Time", "X Motor Axis", "Y Motor Axis", "Z Motor Axis", "X1 Motor", "X2 Motor", "Y1 Motor",
                 "Y2 Motor", "Spindle Voltage", "Raw Load 1", "Raw Load 2", "Raw Load 3", "Raw Load 4", "Raw Load 5",
                 "Average Load 1", "Average Load 2", "Average Load 3", "Average Load 4", "Average Load 5",
                 "Calculated Load", "Target Load", "Raw Multiplier", "Line #", "GCode", "GCode Feed", "Feed Override % Status",
                 "Target Feed", "Actual Feed", "Difference", "Accelerating", "G0 Move", "Allow FeedUp", "Moving in Z",
                 "Raw Multiplier", "Capped Multiplier", "Adjustment List", "Feed Override % Status", "Target Spindle Speed",
                 "Spindle Override %", "Spindle RPM"]]

        for log in self.logs:
            data.append([
                log.time, log.sg_x_motor_axis, log.sg_y_axis, log.sg_z_motor_axis, log.sg_x1_motor, log.sg_x2_motor,
                log.sg_y1_motor, log.sg_y2_motor, log.spindle_voltage, limit(get_safe(log.raw_loads, 0)),
                limit(get_safe(log.raw_loads, 1)), limit(get_safe(log.raw_loads, 2)), limit(get_safe(log.raw_loads, 3)),
                limit(get_safe(log.raw_loads, 4)), limit(get_safe(log.average_loads, 0)), limit(get_safe(log.average_loads, 1)),
                limit(get_safe(log.average_loads, 2)), limit(get_safe(log.average_loads, 3)), limit(get_safe(log.average_loads, 4)),
                limit(log.current_load), log.target_load, limit(log.raw_multiplier), log.line_number, log.gcode, log.gcode_feed,
                log.feed_override_percentage, log.target_feed, int(log.feed_rate), log.target_feed - int(log.feed_rate),
                not log.constant_speed, log.g0_move, log.allow_feedup, log.moving_in_z, log.raw_multiplier,
                log.feed_multiplier, log.adjustment_list, log.feed_override_percentage, log.target_spindle_speed,
                log.spindle_override_percentage, log.spindle_rpm
            ])

        return data

    def get_data_for_chart_data_sheet(self):
        data = [["Time", "X Motor Axis", "Y Motor Axis", "Z Motor Axis", "X1 Motor", "X2 Motor", "Y1 Motor",
                 "Y2 Motor", "Calculated Load", "Target Load", "Raw Multiplier", "GCode Feed", "Feed Override % Status",
                 "Target Feed", "Actual Feed", "Capped Multiplier", "Spindle RPM"]]

        for log in self.logs:
            data.append([
                log.time, log.sg_x_motor_axis, log.sg_y_axis, log.sg_z_motor_axis, log.sg_x1_motor, log.sg_x2_motor,
                log.sg_y1_motor, log.sg_y2_motor, log.current_load, log.target_load, log.raw_multiplier, log.gcode_feed,
                log.feed_override_percentage, log.target_feed, log.feed_rate, log.feed_multiplier, log.spindle_rpm
            ])

        return data

    def get_feed_multiplier(self, current_power):
        if not self.autopilot_instance:
            return 5

        multiplier = self.autopilot_instance.get_multiplier(current_power)

        if multiplier > self.increase_cap:
            return self.increase_cap

        if multiplier < self.decrease_cap:
            return self.decrease_cap

        return multiplier

    def get_sweep(self):
        sweep = [["Spindle Load", "Feed Multiplier"]]
        for power in range(0, 1750):
            multiplier = self.get_feed_multiplier(power)
            sweep.append([power, multiplier])
        return sweep

    def get_parameter_format(self):
        return [
            ["Spindle Mains Voltage", self.autopilot_instance.digital_spindle_mains_voltage],
            ["Spindle Target Watts", self.spindle_target_watts],
            ["Bias for Feed Increase", self.increase_bias],
            ["Bias for Feed Decrease", self.decrease_bias],
            ["M Coefficient", self.m_coefficient],
            ["C Coefficient", self.c_coefficient],
            ["Cap for Feed Increase", self.increase_cap],
            ["Cap for Feed Decrease", self.decrease_cap],
            ["Delay Between Feed Adjustments", self.delay_between_feed_adjustments],
            ["Outlier Amount", self.outlier_amount],
            ["Cap for Feed-Up Change When Moving in Z", self.cap_for_feed_increase_during_z_movement],
            ["Job Start Time", self.job_start_time]
        ]

    def get_parameters(self):
        parameter_file_location = "asmcnc/job/yetipilot/config/algorithm_parameters.json"

        with open(parameter_file_location) as json_file:
            data = json.load(json_file)["Parameters"]

            parameter_format = [[parameter['Name'], parameter['Value']] for parameter in data]

            parameter_format.append(["Spindle Mains Voltage", self.autopilot_instance.digital_spindle_mains_voltage])
            parameter_format.append(["Job Start Time", self.job_start_time])
            parameter_format.append(["Branch", self.autopilot_instance.m.sett.sw_branch])
            parameter_format.append(["Commit", self.autopilot_instance.m.sett.sw_hash])

            return parameter_format

    def export_to_gsheet(self):
        if len(self.logs) == 0:
            return

        export_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = export_time + '-' + self.job_name + '-' + str(self.serial_number)
        yetipilot_exporter.run(title, self)
        self.reset()
        self.exported = True

    def reset(self):
        self.logs[:] = []
        self.exported = False


def get_random_time():
    hours = randint(1, 23)
    minutes = randint(1, 59)
    seconds = randint(1, 59)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)


if __name__ == '__main__':
    logger = AutoPilotLogger(
        spindle_v_main=240,
        spindle_target_watts=1000,
        increase_bias=1.1,
        decrease_bias=0.9,
        m_coefficient=0.0001,
        c_coefficient=0.0001,
        increase_cap=1.5,
        decrease_cap=0.5,
        delay_between_feed_adjustments=0.5,
        outlier_amount=0.5,
        cap_for_feed_increase_during_z_movement=1.5,
        job_name='Test Job',
        serial_number=1234,
        autopilot_instance=None,
        job_start_time=get_random_time())

    time = datetime.datetime.now()

    for i in range(5):
        log_time = time + datetime.timedelta(seconds=i)

        logger.add_log(
            current_load=1000,
            target_load=1000,
            raw_loads=[1000, 1000, 1000, 1000, 1000],
            average_loads=[1000, 1000, 1000, 1000, 1000],
            raw_multiplier=1,
            feed_multiplier=1,
            adjustment_list=[1, 1, 1, 1, 1],
            moving_in_z=False,
            feed_override_percentage=100,
            sg_x_motor_axis=0,
            sg_y_axis=0,
            sg_z_motor_axis=0,
            sg_x1_motor=0,
            sg_x2_motor=0,
            sg_y1_motor=0,
            sg_y2_motor=0,
            raw_spindle_load=1000,
            spindle_voltage=240,
            feed_rate=1000,
            line_number=1,
            gcode_feed=1000,
            target_feed=1000,
            constant_speed=1000,
            time=log_time.strftime('%H:%M:%S'),
            g0_move=False,
            allow_feedup=True
        )

    logger.export_to_gsheet()
