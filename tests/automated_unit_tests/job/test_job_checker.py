from mock import mock
from mock.mock import mock_open

from asmcnc.comms.router_machine import Axis
from asmcnc.geometry.job_envelope import BoundingBox
from asmcnc.job.job_checker import JobChecker
from automated_unit_tests.unit_test_base import UnitTestBase


class TestJobChecker(UnitTestBase):
    def setUp(self):
        super(TestJobChecker, self).setUp()
        self._create_modules()
        self.job_checker = JobChecker(self._router_machine_module, self._localization_module)

    def test_get_axis_max_travel(self):
        self.assertEqual(1499.0, self.job_checker.get_axis_max_travel(Axis.X))
        self.assertEqual(2999.0, self.job_checker.get_axis_max_travel(Axis.Y))
        self.assertEqual(299.0, self.job_checker.get_axis_max_travel(Axis.Z))

    def test_get_job_bounds(self):
        # This gcode is a rectangle with dimensions of x:20, y:25 and z:1
        rect = """
        G00 X0 Y0 F70
        G01 Z-1 F50
        G01 X0 Y20 F50
        G01 X25 Y20
        G01 X25 Y0
        G01 X0 Y0
        G00 Z0 F70
        M30
        """

        with mock.patch("__builtin__.open", mock_open(read_data=rect)) as mock_file:
            bounding_box = BoundingBox()
            bounding_box.set_job_envelope("test")

        self.assertEqual((0.0, 25.0), self.job_checker.get_job_bounds(bounding_box, Axis.X))
        self.assertEqual((0.0, 20.0), self.job_checker.get_job_bounds(bounding_box, Axis.Y))
        self.assertEqual((-1.0, 0.0), self.job_checker.get_job_bounds(bounding_box, Axis.Z))

    def test_is_job_within_bounds(self):
        rect_within_bounds = """
        G00 X5 Y5 F70
        G01 Z-10 F50
        G01 X5 Y20 F50
        G01 X30 Y25
        G01 X30 Y5
        G01 X5 Y5
        G00 Z5 F70
        M30
        """

        self._serial_connection_module.wco_x = -1500.0
        self._serial_connection_module.wco_y = -1500.0
        self._serial_connection_module.wco_z = -20.0

        with mock.patch("__builtin__.open", mock_open(read_data=rect_within_bounds)):
            self.assertEqual([], self.job_checker.is_job_out_of_bounds("test"))

        rect_out_of_bounds = """
        G00 X0 Y0 F70
        G01 Z-1 F50
        G01 X0 Y1500 F50
        G01 X3000 Y1500
        G01 X3000 Y0
        G01 X0 Y0
        G00 Z0 F70
        M30
        """

        with mock.patch("__builtin__.open", mock_open(read_data=rect_out_of_bounds)):
            self.assertEqual(3, len(self.job_checker.is_job_out_of_bounds("test")))