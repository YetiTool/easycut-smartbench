from tests.automated_unit_tests.unit_test_base import UnitTestBase
from parameterized import parameterized #python -m pip install parameterized


class TestRouterMachineSpindleRpm(UnitTestBase):

    def setUp(self):
        super(TestRouterMachineSpindleRpm, self).setUp()
        self._create_modules()

    @parameterized.expand([
        # Target RPM, expected 120V compensated RPM, expected 230V compensated RPM
        # See https://docs.google.com/spreadsheets/d/1Dbn6JmNCWaCNxpXMXxxNB2IKvNlhND6zz_qQlq60dQY/edit#gid=1507195715
        [1000, 0, 0],
        [2000, 0, 0],
        [3000, 0, 0],
        [4000, 0, 2204],
        [5000, 0, 3247],
        [6000, 0, 4289],
        [7000, 0, 5332],
        [8000, 0, 6374],
        [9000, 0, 7417],
        [10000, 1991, 8460],
        [15000, 9411, 13673],
        [25000, 24250, 24098]
    ])
    def test_correct_rpm(self, target_rpm, expected_outcome_120v, expected_outcome_230v):
        self.assertEqual(self._router_machine_module.correct_rpm(target_rpm, 120), expected_outcome_120v)
        self.assertEqual(self._router_machine_module.correct_rpm(target_rpm, 230), expected_outcome_230v)