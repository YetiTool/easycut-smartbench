import unittest
from engine import GCodeEngine

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = GCodeEngine(None)

    def test_rectangle_coordinates(self):
        # Case 1, valid input
        x, y = 100, 100
        expected_output = [(0, 0), (0, y), (x, y), (x, 0)] # BL -> TL -> TR -> BR 
        output = self.engine.rectangle_coordinates(x, y)
        self.assertEqual(output, expected_output)

        # Case 2, invalid input
        x, y = 0, 100
        expected_output = None
        output = self.engine.rectangle_coordinates(x, y)
        self.assertEqual(output, expected_output)

    def test_find_centre(self):
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # Snuck in a duplicate at the end
        expected_output = (50, 50)
        output = self.engine.find_centre(coordinates)
        self.assertEqual(output, expected_output)

    def test_find_corner_rads(self):
        # Case 1
        output = self.engine.find_corner_rads(0.05)
        self.assertFalse(output)

        # Case 2
        output = self.engine.find_corner_rads(0.5)
        self.assertTrue(output)

    def test_is_clockwise(self):
        # Case 1
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # BL -> BR -> TR -> TL -> BL, clockwise
        self.assertTrue(self.engine.is_clockwise(coordinates))

        # Case 2
        coordinates = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # TL -> BL -> BR -> TR -> TL, counter-clockwise
        self.assertFalse(self.engine.is_clockwise(coordinates))

    def test_correct_orientation(self):
        # Case 1
        coordinates = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # TL -> BL -> BR -> TR -> TL, counter-clockwise
        expected_output = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # BL -> BR -> TR -> TL -> BL, clockwise
        output = self.engine.correct_orientation(coordinates, self.engine.is_clockwise(coordinates))
        self.assertEqual(output, expected_output)

        # Case 2
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # BL -> BR -> TR -> TL -> BL, clockwise
        expected_output = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # BL -> BR -> TR -> TL -> BL, clockwise
        output = self.engine.correct_orientation(coordinates, self.engine.is_clockwise(coordinates))
        self.assertEqual(output, expected_output)

    def test_replace_cut_depth_and_z_safe_distance(self):
        gcode_lines = ["G1 X10 Y10 Z10", "G1 X20 Y20 Z-5", "G1 X30 Y30 Z-2"]
        processing_args= {
            "gcode_cut_depth": -5,
            "gcode_z_safe_distance": 10,
            "new_cut_depth": -8,
            "new_z_safe_distance": 5
        }

        expected_output = ["G1 X10 Y10 Z5", "G1 X20 Y20 Z-8", "G1 X30 Y30 Z-2"]
        output = self.engine.replace_cut_depth_and_z_safe_distance(gcode_lines, **processing_args)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()