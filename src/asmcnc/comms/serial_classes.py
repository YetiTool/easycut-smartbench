"""
@author archiejarvis on 07/07/2023
"""

from dataclasses import dataclass


@dataclass
class MachinePosition:
    __slots__ = ["x", "y", "z", "x_change", "y_change", "z_change"]

    x: float
    y: float
    z: float

    x_change: bool
    y_change: bool
    z_change: bool


@dataclass
class WorkPosition:
    __slots__ = ["x", "y", "z"]

    x: float
    y: float
    z: float


@dataclass
class WorkCoordinateOffset:
    __slots__ = ["x", "y", "z"]

    x: float
    y: float
    z: float


@dataclass
class BufferInfo:
    __slots__ = [
        "serial_chars_available",
        "serial_blocks_available",
        "print_buffer_status",
    ]

    serial_chars_available: int
    serial_blocks_available: int
    print_buffer_status: bool


@dataclass
class PinInfo:
    __slots__ = [
        "limit_x",
        "limit_X",
        "limit_y",
        "limit_Y",
        "limit_z",
        "probe",
        "spare_door",
        "dust_shoe_cover",
        "limit_Y_axis",
        "stall_X",
        "stall_Y",
        "stall_Z",
    ]

    limit_x: bool
    limit_X: bool
    limit_y: bool
    limit_Y: bool
    limit_z: bool
    probe: bool
    spare_door: bool
    dust_shoe_cover: bool
    limit_Y_axis: bool
    stall_X: bool
    stall_Y: bool
    stall_Z: bool


@dataclass
class DigitalSpindle:
    __slots__ = [
        "ld_qdA",
        "temperature",
        "kill_time",
        "mains_voltage",
        "in_inrush",
        "inrush_counter",
        "inrush_max",
    ]

    ld_qdA: int
    temperature: int
    kill_time: int
    mains_voltage: int

    in_inrush: bool
    inrush_counter: int
    inrush_max: int


@dataclass
class AnalogSpindle:
    __slots__ = ["load_voltage"]

    load_voltage: float


@dataclass
class FeedsAndSpeeds:
    __slots__ = ["feed_rate", "spindle_speed", "feed_override", "speed_override"]

    feed_rate: float
    spindle_speed: float

    feed_override: int
    speed_override: int


@dataclass
class Temperatures:
    __slots__ = ["motor_driver", "pcb", "transistor_heatsink"]

    motor_driver: float
    pcb: float
    transistor_heatsink: float


@dataclass
class Voltages:
    __slots__ = ["microcontroller_mV", "LED_mV", "PSU_mV", "spindle_speed_monitor_mV"]

    microcontroller_mV: float
    LED_mV: float
    PSU_mV: float
    spindle_speed_monitor_mV: float


@dataclass
class LastStall:
    __slots__ = [
        "tmc_index",
        "motor_step_size",
        "load",
        "threshold",
        "travel_distance",
        "temperature",
        "x_coord",
        "y_coord",
        "z_coord",
        "status",
    ]

    tmc_index: int
    motor_step_size: int
    load: int
    threshold: int
    travel_distance: int
    temperature: int
    x_coord: float
    y_coord: float
    z_coord: float
    status: str


@dataclass
class StallGuard:
    __slots__ = [
        "x_motor_axis",
        "z_motor_axis",
        "y_axis",
        "y1_motor",
        "y2_motor",
        "x1_motor",
        "x2_motor",
        "last_stall",
    ]

    x_motor_axis: int
    z_motor_axis: int
    y_axis: int
    y1_motor: int
    y2_motor: int
    x1_motor: int
    x2_motor: int
    last_stall: LastStall


@dataclass
class SpindleStatistics:
    __slots__ = [
        "serial_number",
        "production_year",
        "production_week",
        "firmware_version",
        "total_run_time_seconds",
        "brush_run_time_seconds",
        "mains_frequency_hertz",
    ]

    serial_number: int
    production_year: int
    production_week: int
    total_run_time_seconds: int
    brush_run_time_seconds: int
    mains_frequency_hertz: int


@dataclass
class TMCRegisters:
    __slots__ = [
        "tmc_0",
        "tmc_1",
        "tmc_2",
        "tmc_3",
        "tmc_4",
        "tmc_5",
        "active_current_scale",
        "stand_still_current_scale",
        "stall_guard_alarm_threshold",
        "max_step_period_us_SG",
        "temperature_coefficient",
        "got_registers",
    ]

    tmc_0: int
    tmc_1: int
    tmc_2: int
    tmc_3: int
    tmc_4: int
    tmc_5: int
    active_current_scale: int
    stand_still_current_scale: int
    stall_guard_alarm_threshold: int
    max_step_period_us_SG: int
    temperature_coefficient: int
    got_registers: bool


@dataclass
class Settings:
    def store_variable(self, variable, value):
        setattr(self, "s" + str(variable), value)

    def get_variable(self, variable):
        return getattr(self, "s" + str(variable))


@dataclass
class G28:
    __slots__ = ["x", "y", "z"]

    x: float
    y: float
    z: float


@dataclass
class G54:
    __slots__ = ["x", "y", "z"]

    x: float
    y: float
    z: float


@dataclass
class Versions:
    __slots__ = ["firmware", "hardware"]

    firmware: str
    hardware: str
