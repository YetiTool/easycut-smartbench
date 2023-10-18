import calibration_database

db = calibration_database.CalibrationDatabase()
db.set_up_connection()


def test_do_z_head_coefficients_exist():
    assert db.do_z_head_coefficients_exist(167701)
    assert not db.do_z_head_coefficients_exist(991101)


def test_do_lower_beam_coefficients_exist():
    assert db.do_lower_beam_coefficients_exist(142926)
    assert not db.do_lower_beam_coefficients_exist(991101)
