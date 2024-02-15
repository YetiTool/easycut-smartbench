from asmcnc.comms import model_detector
from automated_unit_tests.unit_test_base import UnitTestBase


class TestLocalizationProductName(UnitTestBase):
    def setUp(self):
        super(TestLocalizationProductName, self).setUp()

    def test_get_str(self):
        # Patch model_detector.is_machine_drywall to return False
        model_detector.is_machine_drywall = lambda: False

        # Create the localization module
        self._localization_module = self._create_localization_module()

        # Set the dictionary to a single entry, "SmartBench": "SmartBench"
        self._localization_module.dictionary = {
            "SmartBench": "SmartBench",
        }

        # Test that the get_str method returns the value from the dictionary
        self.assertEqual(self._localization_module.get_str("SmartBench"), "SmartBench")

        # Patch model_detector.is_machine_drywall to return True
        model_detector.is_machine_drywall = lambda: True

        # Recreate the localization module (to update the PRODUCT_NAME)
        self._localization_module = self._create_localization_module()

        # Test that the get_str method returns the value from the dictionary, with the PRODUCT_NAME replaced
        self.assertEqual(self._localization_module.get_str("SmartBench"), "SmartCNC")
