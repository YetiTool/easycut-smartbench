import json
import os

from mock import mock
from mock.mock import Mock

from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app.config.config_classes import Configuration
from automated_unit_tests.unit_test_base import UnitTestBase


class ConfigLoaderTestCases(UnitTestBase):
    def setUp(self):
        super(ConfigLoaderTestCases, self).setUp()
        self.dwt_config = config_loader.DWTConfig(Mock())

    def test_get_most_recent_config(self):
        with mock.patch("os.listdir") as mocked_listdir:
            mocked_listdir.return_value = ["test_config", "test_config2"]
            with mock.patch("os.path.getmtime") as mocked_getmtime:
                mocked_getmtime.return_value = 100

                self.assertEqual(self.dwt_config.get_most_recent_config().split(os.sep)[-1], "test_config")

            mocked_listdir.return_value = []

            self.assertEqual(self.dwt_config.get_most_recent_config(), None)

    def test_start_up(self):
        # Mock os.listdir so
        with mock.patch("os.listdir") as mocked_listdir:
            mocked_listdir.return_value = []

            # Test loading DEFAULT Configuration if temp_config doesn't exist, and there's no recent configs
            with mock.patch("os.path.exists") as mocked_exists:
                mocked_exists.return_value = False
                self.dwt_config.start_up()
                self.assertEqual(json.dumps(self.dwt_config.active_config, default=lambda o: o.__dict__), json.dumps(Configuration.default(), default=lambda o: o.__dict__))

            # Test loading temp config, if there's no recent configs but temp_config does exist
            self.dwt_config.start_up()
            with open(config_loader.TEMP_CONFIG_PATH, 'r') as f:
                # Want to compare the entire thing, but had trouble so this is probably sufficient
                f_contents = f.read()
                self.assertEqual(self.dwt_config.active_config.canvas_shape_dims.x, json.loads(f_contents)["canvas_shape_dims"]["x"])
                self.assertEqual(self.dwt_config.active_config.cutter_type, json.loads(f_contents)["cutter_type"])
