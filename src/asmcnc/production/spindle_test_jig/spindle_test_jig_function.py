from kivy.clock import Clock
from asmcnc.production.spindle_test_jig.popups.post_test_summary_popup import PostTestSummaryPopup
from math import sqrt


def ld_qda_to_w(voltage, ld_qda):
    return voltage * 0.1 * sqrt(ld_qda)


class SpindleTest:
    test_pass = None
    fail_reasons = []
    spindle_load_samples = []
    clocks = []
    target_voltage = None

    def __init__(self, **kwargs):
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.screen = kwargs['screen']

    def add_spindle_load(self):
        if len(self.spindle_load_samples) == 5:
            self.spindle_load_samples.pop(0)

        load = ld_qda_to_w(self.m.s.digital_spindle_mains_voltage,
                           self.m.s.digital_spindle_ld_qdA)
        self.spindle_load_samples.append(load)

    def run(self):
        self.screen.run_test_button.disabled = True
        self.fail_reasons[:] = []

        def show_result():
            PostTestSummaryPopup(self.m, self.sm, self.fail_reasons)

            if len(self.fail_reasons) > 0:
                self.screen.pass_fail_img.source = 'asmcnc/apps/start_up_sequence/data_consent_app/img/red_cross.png'
                return

            self.screen.pass_fail_img.source = 'asmcnc/skavaUI/img/green_tick.png'

        def fail_test(rpm, reason):
            self.test_pass = False
            self.fail_reasons.append([rpm, reason])

        def check(rpm):
            measured_rpm = self.m.convert_from_110_to_230(int(self.m.s.spindle_speed))
            measured_voltage = self.m.s.digital_spindle_mains_voltage
            measured_temp = self.m.s.digital_spindle_temperature
            measured_kill_time = self.m.s.digital_spindle_kill_time
            measured_load = sum(self.spindle_load_samples) / len(self.spindle_load_samples)

            if abs(rpm - measured_rpm) > 2000:
                fail_test(rpm, "RPM out of range: " + str(measured_rpm))

            if abs(self.target_voltage - measured_voltage) > 15:
                fail_test(rpm, "Voltage out of range: " + str(measured_voltage))

            if measured_temp < 10 or measured_temp > 40:
                fail_test(rpm, "Temperature out of range: " + str(measured_temp))

            if not (measured_kill_time > 254):
                fail_test(rpm, "Kill time out of range: " + str(measured_kill_time))

            if measured_load < 100 or measured_load > 400:
                fail_test(rpm, "Load out of range: " + str(measured_load))

        def set_rpm(rpm):
            self.m.s.write_command('M3 S' + str(rpm))
            self.screen.target_rpm_value.text = str(rpm)
            self.clocks.append(Clock.schedule_once(lambda dt: check(rpm), 1.5))

        self.clocks[:] = []
        set_rpm(10000)
        self.clocks.append(Clock.schedule_once(lambda dt: set_rpm(13000), 3))
        self.clocks.append(Clock.schedule_once(lambda dt: set_rpm(19000), 6))
        self.clocks.append(Clock.schedule_once(lambda dt: set_rpm(22000), 9))
        self.clocks.append(Clock.schedule_once(lambda dt: set_rpm(25000), 12))
        self.clocks.append(Clock.schedule_once(lambda dt: set_rpm(0), 15))
        self.clocks.append(Clock.schedule_once(lambda dt: show_result(), 15))
        self.clocks.append(Clock.schedule_once(lambda dt: self.screen.toggle_run_button(), 15))


