class ZHeadStatistic(object):
    zh_serial = None
    fw_version = None #
    hw_version = None #
    chip_id = None
    cpu_v = None #
    led_v = None #
    main_v = None #
    spindle_load_2 = None
    spindle_load_3 = None
    spindle_load_4 = None
    spindle_load_5 = None
    max_spindle_speed_control = None
    cpu_temp = None #
    pcb_temp = None #
    tmc_temp = None #
    tmc_x_status_bits = None
    tmc_x2_status_bits = None
    tmc_z_status_bits = None
    tmc_x_raw_sg = None #
    tmc_x2_raw_sg = None
    tmc_z_raw_sg = None #
    v_main = None
    f_main = None
    set_rpm = None #
    measured_rpm = None #
    idle_load = None

    def get_params(self):
        return (self.zh_serial, self.fw_version, self.hw_version, self.chip_id, self.cpu_v,
                self.led_v, self.main_v, self.spindle_load_2, self.spindle_load_3,
                self.spindle_load_4, self.spindle_load_5, self.max_spindle_speed_control,
                self.cpu_temp, self.pcb_temp, self.tmc_temp, self.tmc_x_status_bits,
                self.tmc_z_status_bits, self.tmc_x2_status_bits, self.tmc_x_raw_sg, self.tmc_x2_raw_sg,
                self.tmc_z_raw_sg, self.v_main, self.f_main, self.set_rpm, self.measured_rpm, self.idle_load)
