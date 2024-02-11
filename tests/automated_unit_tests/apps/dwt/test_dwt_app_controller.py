from asmcnc.apps.drywall_cutter_app.dwt_app_controller import DrywallCutterController
from automated_unit_tests.unit_test_base import UnitTestBase


class TestDWTAppController(UnitTestBase):
    def setUp(self):
        super(TestDWTAppController, self).setUp()
        self._create_modules()
        self.__app_controller = DrywallCutterController(
            name='drywall_cutter', machine=self._router_machine_module,
            screen_manager=self._screen_manager, keyboard=self._keyboard_module,
            localization=self._localization_module, job_data=self._job_data_module
        )

    def test_get_screen(self):
        screen = self.__app_controller.get_screen()
        self.assertIsNotNone(screen)

    def test_load_default_state(self):
        pass

    def test_handle_cutter_selection_changed(self):
        test_cutter = self.__app_controller.model.config.cutter_options.keys()[0]

        self.__app_controller.handle_cutter_selection_changed(test_cutter)

        assert self.__app_controller.model.config.active_config.cutter_type == test_cutter
