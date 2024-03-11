import unittest
from engine import GCodeEngine

class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = GCodeEngine(None)

    def test_replace_cut_depth_and_z_safe_distance(self):
        gcode_lines = ["G1 X10 Y10 Z10", "G1 X20 Y20 Z-5", "G1 X30 Y30 Z-2"]
        gcode_cut_depth = -5
        gcode_z_safe_distance = 10
        new_cut_depth = -8
        new_z_safe_distance = 5

        expected_output = ["G1 X10 Y10 Z5", "G1 X20 Y20 Z-8", "G1 X30 Y30 Z-2"]
        output = self.engine.replace_cut_depth_and_z_safe_distance(gcode_lines, gcode_cut_depth, gcode_z_safe_distance, new_cut_depth, new_z_safe_distance)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()