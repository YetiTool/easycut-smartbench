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

    def test_add_corner_coordinates(self):
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)]
        corner_radius = 10
        expected_output = [(10, 0), (0, 10), (100.0, 10), (90.0, 0), (90.0, 100.0), (100.0, 90.0), (0, 90.0), (10, 100.0), (10, 0), (0, 10)]
        output = self.engine.add_corner_coordinates(coordinates, self.engine.find_centre(coordinates), corner_radius)
        self.assertEqual(output, expected_output)

    def test_calculate_corner_radius_offset(self):
        tool_diameter = 10

        offset_type = "inside"
        expected_output = -5
        output = self.engine.calculate_corner_radius_offset(offset_type, tool_diameter)
        self.assertEqual(output, expected_output)
    
        offset_type = "outside"
        expected_output = 5
        output = self.engine.calculate_corner_radius_offset(offset_type, tool_diameter)
        self.assertEqual(output, expected_output)

        offset_type = "invalid input"
        expected_output = 0
        output = self.engine.calculate_corner_radius_offset(offset_type, tool_diameter)
        self.assertEqual(output, expected_output)

    def test_apply_offset(self):
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)]
        shape_centre = (50, 50)
        tool_diameter = 10
        
        offset_type = "inside"
        expected_output = [(5, 5), (95, 5), (95, 95), (5, 95), (5, 5)]
        # Convert to floats
        expected_output = [(float(x), float(y)) for x, y in expected_output]
        output = self.engine.apply_offset(coordinates, offset_type, tool_diameter, shape_centre)
        self.assertEqual(output, expected_output)

        offset_type = "outside"
        expected_output = [(-5, -5), (105, -5), (105, 105), (-5, 105), (-5, -5)]
        # Convert to floats
        expected_output = [(float(x), float(y)) for x, y in expected_output]
        output = self.engine.apply_offset(coordinates, offset_type, tool_diameter, shape_centre)
        self.assertEqual(output, expected_output)

        offset_type = None
        expected_output = coordinates
        # Convert to floats
        expected_output = [(float(x), float(y)) for x, y in expected_output]
        output = self.engine.apply_offset(coordinates, offset_type, tool_diameter, shape_centre)
        self.assertEqual(output, expected_output)

    def test_calculate_pass_depths(self):
        # Case 1: total_cut_depth is divisible by pass_depth
        total_cut_depth = 10
        pass_depth = 2
        expected_output = [2, 4, 6, 8, 10]
        output = self.engine.calculate_pass_depths(total_cut_depth, pass_depth)
        self.assertEqual(output, expected_output)

        # Case 2: total_cut_depth is not divisible by pass_depth
        total_cut_depth = 12
        pass_depth = 5
        expected_output = [5, 10, 12]
        output = self.engine.calculate_pass_depths(total_cut_depth, pass_depth)
        self.assertEqual(output, expected_output)

        # Case 3: total_cut_depth is equal to pass_depth
        total_cut_depth = 5
        pass_depth = 5
        expected_output = [5]
        output = self.engine.calculate_pass_depths(total_cut_depth, pass_depth)
        self.assertEqual(output, expected_output)

        # Case 4: total_cut_depth is less than pass_depth
        total_cut_depth = 2
        pass_depth = 5
        expected_output = [2]
        output = self.engine.calculate_pass_depths(total_cut_depth, pass_depth)
        self.assertEqual(output, expected_output)

    def test_determine_cut_direction_clockwise(self):
        # Case 1: climb=True, offset_type="outside"
        offset_type = "outside"
        climb = True
        expected_output = True
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)

        # Case 2: climb=False, offset_type="inside"
        offset_type = "inside"
        climb = False
        expected_output = True
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)

        # Case 3: climb=True, offset_type="inside"
        offset_type = "inside"
        climb = True
        expected_output = False
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)

        # Case 4: climb=False, offset_type="outside"
        offset_type = "outside"
        climb = False
        expected_output = False
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()