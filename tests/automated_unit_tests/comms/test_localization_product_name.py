import logging
from mock import patch
from tests.automated_unit_tests.unit_test_base import UnitTestBase


class TestLocalizationProductName(UnitTestBase):

    def setUp(self):
        super(TestLocalizationProductName, self).setUp()

    @patch(
        'src.asmcnc.comms.model_manager.ModelManagerSingleton.is_machine_drywall'
        )
    def test_get_str(self, mock_is_machine_drywall):
        mock_is_machine_drywall.return_value = False
        self._localization_module = self._create_localization_module()
        self._localization_module.dictionary = {'SmartBench': 'SmartBench'}
        self.assertEqual(self._localization_module.get_str('SmartBench'),
            'SmartBench')
        mock_is_machine_drywall.return_value = True
        self._localization_module = self._create_localization_module()
        self.assertEqual(self._localization_module.get_str('SmartBench'),
            'SmartCNC')
