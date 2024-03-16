import sys, os

from asmcnc.comms.logging_system.logging_system import Logger

sys.path.append('./src')

try: 
    import unittest
    import pytest
    from mock import Mock, MagicMock

except: 
    Logger.info("Can't import mocking packages, are you on a dev machine?")

from asmcnc.job import job_data
from asmcnc.comms import localization
from datetime import datetime

from kivy.clock import Clock

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/job/test_generate_recovery_gcode.py
######################################
'''

# FIXTURES
@pytest.fixture
def jd():
    l = localization.Localization()
    settings_manager = Mock()
    jd = job_data.JobData(localization = l, settings_manager = settings_manager)
    return jd


# GCODE GENERATION

def test_coordinate_system_select(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "G1G54X6.776G1",
        "X6.776Y6.776Z-0.720F769.25",
        "G1G55.1X6.776G1",
        "X2.259Y2.259Z-0.240F796.74",
        "G1G56X6.776G1",
        "X2.259Y2.259Z-0.240F824.88",
        "G1G57.2",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]

    jd.job_recovery_selected_line = 11
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G59.3",
        "G90",
        "G0 X6.776 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == -6

    jd.job_recovery_selected_line = 10
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G58",
        "G90",
        "G0 X6.776 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == -5

    jd.job_recovery_selected_line = 9
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G57.2",
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == -4

    jd.job_recovery_selected_line = 8
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G56",
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G1G57.2",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == -3

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G55.1",
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F796.74",
        "G1G56X6.776G1",
        "X2.259Y2.259Z-0.240F824.88",
        "G1G57.2",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G54",
        "G90",
        "G0 X6.776 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "G1G55.1X6.776G1",
        "X2.259Y2.259Z-0.240F796.74",
        "G1G56X6.776G1",
        "X2.259Y2.259Z-0.240F824.88",
        "G1G57.2",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "G1G54X6.776G1",
        "X6.776Y6.776Z-0.720F769.25",
        "G1G55.1X6.776G1",
        "X2.259Y2.259Z-0.240F796.74",
        "G1G56X6.776G1",
        "X2.259Y2.259Z-0.240F824.88",
        "G1G57.2",
        "G58X6.776G1",
        "G59.3",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_plane_selection(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "X2G17Y20.2597",
        "G18X2.259",
        "G19",
        "M5"
    ]

    jd.job_recovery_selected_line = 8
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G19",
        "G90",
        "G0 X2.259 Y20.2597",
        "G0 Z-0.240",
        "G1 F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == -3

    jd.job_recovery_selected_line = 7
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G18",
        "G90",
        "G0 X2.259 Y20.2597",
        "G0 Z-0.240",
        "G1 F824.88",
        "G19",
        "M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G17",
        "G90",
        "G0 X2 Y20.2597",
        "G0 Z-0.240",
        "G1 F824.88",
        "G18X2.259",
        "G19",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "X2G17Y20.2597",
        "G18X2.259",
        "G19",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

def test_absolute_or_incremental_distance_mode(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "G91",
        "M5"
    ]

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'The last positioning declaration was incremental (G91), and therefore this job cannot be recovered.'

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G91",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "G91",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_arc_ijk_distance_mode(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "G90.1",
        "G91.1",
        "M5"
    ]

    jd.job_recovery_selected_line = 7
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'Job recovery does not currently support arc distance modes. This job contains G91.1, and therefore cannot be recovered.'

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'Job recovery does not currently support arc distance modes. This job contains G90.1, and therefore cannot be recovered.'

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G90.1",
        "G91.1",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

def test_feed_rate_mode(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "G93",
        "G94",
        "G95",
        "M5"
    ]

    jd.job_recovery_selected_line = 8
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'Job recovery only supports feed rate mode G94. This job contains G95, and therefore cannot be recovered.'

    jd.job_recovery_selected_line = 7
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G94",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G95",
        "M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'Job recovery only supports feed rate mode G94. This job contains G93, and therefore cannot be recovered.'

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "G93",
        "G94",
        "G95",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

def test_units(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720G20F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259G21Y2.259Z-0.240F824.88",
        "M5"
    ]

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G21",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G20",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F796.74",
        "X2.259G21Y2.259Z-0.240F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "X6.776Y6.776Z-0.720G20F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259G21Y2.259Z-0.240F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_cutter_radius_compensation(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240G40F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "M5"
    ]

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G40",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "X2.259Y2.259Z-0.240G40F796.74",
        "X2.259Y2.259Z-0.240F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_tool_length_offset(jd):
    jd.job_gcode = [
        "G90X0F1000",
        "G1X0F8000",
        "X6.776Y6.776Z-0.720G49F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240G43.1F824.88",
        "M5"
    ]

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G43.1",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G49",
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F796.74",
        "X2.259Y2.259Z-0.240G43.1F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "X6.776Y6.776Z-0.720G49F769.25",
        "X2.259Y2.259Z-0.240F796.74",
        "X2.259Y2.259Z-0.240G43.1F824.88",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_program_mode(jd):
    jd.job_gcode = [
        "G90",
        "M30",
        "M02G",
        "M1G",
        "M20",
        "M00",
        "M5"
    ]

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M00",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M1",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M00",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M1",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M20",
        "M00",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M02",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M1G",
        "M20",
        "M00",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M30",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M02G",
        "M1G",
        "M20",
        "M00",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90",
        "M30",
        "M02G",
        "M1G",
        "M20",
        "M00",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_coolant_state(jd):
    # Various orders and combinations as M7 and M8 can be used simultaneously
    jd.job_gcode = [
        "G90",
        "M8",
        "M09",
        "M07",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]

    jd.job_recovery_selected_line = 11
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M7",
        "M8",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G1"
    ]
    assert jd.job_recovery_offset == -6

    jd.job_recovery_selected_line = 7
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M8",
        "M7",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M8",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M9",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M7",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M9",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M07",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M8",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M09",
        "M07",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90",
        "M8",
        "M09",
        "M07",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == 2

    # Just in case, check M7 is found when nothing is before it, same as M8 two tests above
    jd.job_gcode = ["M07"] + jd.job_gcode
    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M7",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M8",
        "M09",
        "M07",
        "M9",
        "M8",
        "G90M7G90",
        "G90M08G90",
        "M70",
        "M80",
        "M90",
        "G1"
    ]
    assert jd.job_recovery_offset == 2

def test_spindle_speed(jd):
    jd.job_gcode = [
        "S2000",
        "S5000M3",
        "S0",
        "G4 P4",
        "M3 S25000",
        "G4 P4",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]

    jd.job_recovery_selected_line = 9
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S15000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == -5

    jd.job_recovery_selected_line = 8
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S20000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M03",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == -4

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S25000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M3",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S0",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M3",
        "M3 S25000",
        "G4 P4",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S5000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M3",
        "S0",
        "G4 P4",
        "M3 S25000",
        "G4 P4",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 1
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "S2000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "S5000M3",
        "S0",
        "G4 P4",
        "M3 S25000",
        "G4 P4",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "S2000",
        "S5000M3",
        "S0",
        "G4 P4",
        "M3 S25000",
        "G4 P4",
        "M03S20000",
        "G4 P4",
        "S15000 M03",
        "S10000 M5"
    ]
    assert jd.job_recovery_offset == 2

def test_feedrate(jd):
    jd.job_gcode = [
        "G1X0",
        "F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "F796.74X2.259Y2.259Z-0.240",
        "G90F1000X0",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]

    jd.job_recovery_selected_line = 6
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'This job cannot be recovered! Please check your job for errors.'

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "G0 X0 Y2.259",
        "G0 Z-0.240",
        "G1 F1000",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X2.259 Y2.259",
        "G0 Z-0.240",
        "G1 F796.74",
        "G90F1000X0",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]
    assert jd.job_recovery_offset == -1

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X6.776 Y6.776",
        "G0 Z-0.720",
        "G1 F769.25",
        "F796.74X2.259Y2.259Z-0.240",
        "G90F1000X0",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1 F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "F796.74X2.259Y2.259Z-0.240",
        "G90F1000X0",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 1
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0 Y0.000",
        "G0 Z0.000",
        "G1",
        "F8000",
        "X6.776Y6.776Z-0.720F769.25",
        "F796.74X2.259Y2.259Z-0.240",
        "G90F1000X0",
        "X2.259Y2.259Z-0.240F",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_motion_mode(jd):
    jd.job_gcode = [
        "G1 X100",
        "G00 F1000",
        "G01 Y200",
        "G0 Z100",
        "G10",
        "M5"
    ]

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G1 F1000",
        "G0 X100 Y200",
        "G0 Z100",
        "M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X100 Y200",
        "G0 Z0.000",
        "G1 F1000",
        "G0 Z100",
        "G10",
        "M5"
    ]
    assert jd.job_recovery_offset == 0

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G1 F1000",
        "G0 X100 Y0.000",
        "G0 Z0.000",
        "G01 Y200",
        "G0 Z100",
        "G10",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 1
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X100 Y0.000",
        "G0 Z0.000",
        "G1",
        "G00 F1000",
        "G01 Y200",
        "G0 Z100",
        "G10",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G1 X100",
        "G00 F1000",
        "G01 Y200",
        "G0 Z100",
        "G10",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_spindle_state(jd):
    jd.job_gcode = [
        "G90",
        "S20000M3",
        "M04",
        "M30",
        "M5",
        "G1"
    ]

    jd.job_recovery_selected_line = 5
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M30",
        "S20000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M5",
        "G1"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 4
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "M30",
        "S20000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M04",
        "M5",
        "G1"
    ]
    assert jd.job_recovery_offset == 2

    jd.job_recovery_selected_line = 2
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G90",
        "S20000",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "M3",
        "M04",
        "M30",
        "M5",
        "G1"
    ]
    assert jd.job_recovery_offset == 3

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90",
        "S20000M3",
        "M04",
        "M30",
        "M5",
        "G1"
    ]
    assert jd.job_recovery_offset == 2

def test_regular_case(jd):
    jd.job_gcode = [
        "T1",
        "G17",
        "G21",
        "G90",
        "G0Z20.000",
        "G0X0.000Y0.000",
        "S20000M3",
        "G90 G94",
        "G17",
        "G21",
        "G28 G91 Z0",
        "G90",
        "T1",
        "S20000 M3",
        "G54",
        "M8",
        "G0 X548.725 Y263.63",
        "Z12",
        "Z11",
        "G1 Z9.63 F1000",
        "G18 G3 X548.095 Z9 I-0.63 K0",
        "G1 X547.78",
        "G17 G3 X547.15 Y263 I0 J-0.63",
        "M5"
    ]

    jd.job_recovery_selected_line = 23
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G54",
        "G17",
        "G90",
        "G94",
        "G21",
        "M8",
        "S20000",
        "G0 X547.15 Y263",
        "G0 Z9",
        "G1 F1000",
        "M3",
        "M5"
    ]
    assert jd.job_recovery_offset == -12

    jd.job_recovery_selected_line = 10
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G17",
        "G90",
        "G94",
        "G21",
        "S20000",
        "G0 X0.000 Y0.000",
        "G0 Z20.000",
        "M3",
        "G28 G91 Z0",
        "G90",
        "T1",
        "S20000 M3",
        "G54",
        "M8",
        "G0 X548.725 Y263.63",
        "Z12",
        "Z11",
        "G1 Z9.63 F1000",
        "G18 G3 X548.095 Z9 I-0.63 K0",
        "G1 X547.78",
        "G17 G3 X547.15 Y263 I0 J-0.63",
        "M5"
    ]
    assert jd.job_recovery_offset == -2

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G17",
        "G21",
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "G90",
        "G0Z20.000",
        "G0X0.000Y0.000",
        "S20000M3",
        "G90 G94",
        "G17",
        "G21",
        "G28 G91 Z0",
        "G90",
        "T1",
        "S20000 M3",
        "G54",
        "M8",
        "G0 X548.725 Y263.63",
        "Z12",
        "Z11",
        "G1 Z9.63 F1000",
        "G18 G3 X548.095 Z9 I-0.63 K0",
        "G1 X547.78",
        "G17 G3 X547.15 Y263 I0 J-0.63",
        "M5"
    ]
    assert jd.job_recovery_offset == 1

    jd.job_recovery_selected_line = 0
    success, message = jd.generate_recovery_gcode()
    assert success
    assert jd.job_recovery_gcode == [
        "G0 X0.000 Y0.000",
        "G0 Z0.000",
        "T1",
        "G17",
        "G21",
        "G90",
        "G0Z20.000",
        "G0X0.000Y0.000",
        "S20000M3",
        "G90 G94",
        "G17",
        "G21",
        "G28 G91 Z0",
        "G90",
        "T1",
        "S20000 M3",
        "G54",
        "M8",
        "G0 X548.725 Y263.63",
        "Z12",
        "Z11",
        "G1 Z9.63 F1000",
        "G18 G3 X548.095 Z9 I-0.63 K0",
        "G1 X547.78",
        "G17 G3 X547.15 Y263 I0 J-0.63",
        "M5"
    ]
    assert jd.job_recovery_offset == 2

def test_random_gibberish(jd):
    jd.job_gcode = [
        "GDFASGFDATG324534RGE",
        "'#;#FASASD[FKDAOS]'",
        "543QHYTYJEAGFDA",
        "W4A3ERTIUJUSUEXHTDG"
    ]

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert not success
    assert message == 'This job cannot be recovered! Please check your job for errors.'

def test_r_handling(jd):
    jd.job_gcode = [
        "G0 X0 Y2.0",
        "G1 Z-6.0 F400",
        "G3 X2.0 Y0 R2.0 F8000",
        "G1 X23.0 Y0"
    ]

    jd.job_recovery_selected_line = 3
    success, message = jd.generate_recovery_gcode()
    assert success
    # Output should not include the R
    assert jd.job_recovery_gcode == [
        "G0 X2.0 Y0",
        'G0 Z-6.0',
        'G1 F8000',
        'G1 X23.0 Y0'
    ]
    assert jd.job_recovery_offset == 0
