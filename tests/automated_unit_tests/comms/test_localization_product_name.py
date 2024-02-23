from mock import patch

from tests.automated_unit_tests.unit_test_base import UnitTestBase


class TestLocalizationProductName(UnitTestBase):
    def setUp(self):
        super(TestLocalizationProductName, self).setUp()

    @patch('src.asmcnc.comms.model_manager.ModelManagerSingleton.is_machine_drywall')
    def test_get_str(self,mock_is_machine_drywall):
        # Patch model_manager.is_machine_drywall to return False
        mock_is_machine_drywall.return_value = False

        # Create the localization module
        self._localization_module = self._create_localization_module()
        # Set the dictionary to a single entry, "SmartBench": "SmartBench"
        self._localization_module.dictionary = {
            "SmartBench": "SmartBench",
        }

        # Test that the get_str method returns the value from the dictionary
        self.assertEqual(self._localization_module.get_str("SmartBench"), "SmartBench")

        # Patch model_manager.is_machine_drywall to return True
        mock_is_machine_drywall.return_value = True

        # Recreate the localization module (to update the PRODUCT_NAME)
        self._localization_module = self._create_localization_module()

        # Test that the get_str method returns the value from the dictionary, with the PRODUCT_NAME replaced
        self.assertEqual(self._localization_module.get_str("SmartBench"), "SmartCNC")
