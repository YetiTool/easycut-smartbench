import unittest
import sys
import os

easycut_dir = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(easycut_dir, 'src')) # Alternative to sys.path.append("./src") which didn't work me

from apps.drywall_cutter_app.engine import GCodeEngine
from core.serial.router_machine import RouterMachine

'''
To run this test,
from /easyCut-smartbench/tests directory, run:
python test_engine.py
'''

class EngineTests(unittest.TestCase):
    def setUp(self):

        class Cutter:
            def __init__(self):
                self.diameter = 0
                
        class Config:
            def __init__(self, *args, **kwargs):
                self.active_config = self
                self.shape_type = None
                self.active_cutter = kwargs.get('active_cutter')
                self.active_cutter.dimensions.tool_diameter = 10

        dummy_cutter = Cutter()
        dummy_config = Config(active_cutter = dummy_cutter)
        self.engine = GCodeEngine(RouterMachine, dummy_config)

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
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)] # BL -> BR -> TR -> TL -> BL, anti-clockwise
        self.assertFalse(self.engine.is_clockwise(coordinates))

        # Case 2
        coordinates = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # BL, TL, TR, BR, BL, clockwise
        self.assertTrue(self.engine.is_clockwise(coordinates))

    def test_correct_orientation(self):
        # Case 1: No change needed
        coordinates = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # BL, TL, TR, BR, BL, clockwise
        expected_output = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # BL, TL, TR, BR, BL, clockwise
        output = self.engine.correct_orientation(coordinates, self.engine.is_clockwise(coordinates))
        self.assertEqual(output, expected_output)

        # Case 2: Change needed
        coordinates = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # BL, BR, TR, TL, BL, anti-clockwise
        expected_output = [(0, 0), (0, 100.0), (100.0, 100.0), (100.0, 0), (0, 0)] # BL, TL, TR, BR, BL, clockwise
        output = self.engine.correct_orientation(coordinates, self.engine.is_clockwise(coordinates))
        self.assertEqual(output, expected_output)

    def test_add_corner_coordinates(self):
        coordinates = [(0, 0), (100.0, 0), (100.0, 100.0), (0, 100.0), (0, 0)]
        corner_radius = 10
        expected_output = [(0, 10), (10, 0), (90, 0), (100, 10), (100, 90), (90, 100), (10, 100), (0, 90), (0, 10), (10, 0)]
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

        # Case 5: offset_type="on" default to climb
        offset_type = "on"
        climb = False
        expected_output = False
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)
        climb = True
        expected_output = True
        output = self.engine.determine_cut_direction_clockwise(offset_type, climb)
        self.assertEqual(output, expected_output)

        # Case 6: failure
        offset_type = "foo"
        climb = False
        expected_output = False
        with self.assertRaises(ValueError):
            self.engine.determine_cut_direction_clockwise(offset_type, climb)


    def test_swap_lines_after_keyword(self):
        # Case 1: Keyword exists and there are at least two lines after the keyword
        input_list = ["Line 1", "Keyword", "Line 2", "Line 3"]
        keyword = "keyword"
        expected_output = ["Line 1", "Keyword", "Line 3", "Line 2"]
        output = self.engine.swap_lines_after_keyword(input_list, keyword)
        self.assertEqual(output, expected_output)

        # Case 2: Keyword exists but there is only one line after the keyword
        input_list = ["Line 1", "Keyword", "Line 2"]
        keyword = "keyword"
        expected_output = ["Line 1", "Keyword", "Line 2"]
        output = self.engine.swap_lines_after_keyword(input_list, keyword)
        self.assertEqual(output, expected_output)

        # Case 3: Keyword does not exist
        input_list = ["Line 1", "Line 2", "Line 3"]
        keyword = "keyword"
        expected_output = ["Line 1", "Line 2", "Line 3"]
        output = self.engine.swap_lines_after_keyword(input_list, keyword)
        self.assertEqual(output, expected_output)

        # Case 4: Empty input list
        input_list = []
        keyword = "keyword"
        expected_output = []
        output = self.engine.swap_lines_after_keyword(input_list, keyword)
        self.assertEqual(output, expected_output)

    def test_replace_mode_after_keyword(self):
        # Case 1: Keyword exists and there are at least two lines after the keyword
        keyword = "keyword"
        replacement = "G0"
        input_list = ["Line 1", keyword, "G1 X5", "Line 3"]
        expected_output = ["Line 1", keyword, "G0 X5", "Line 3"]
        output = self.engine.replace_mode_after_keyword(input_list, keyword, replacement)
        self.assertEqual(output, expected_output)

        # Case 2: Keyword exists but there is only one line after the keyword
        input_list = ["Line 1", keyword, "G1 X5"]
        expected_output = ["Line 1", keyword, "G0 X5"]
        output = self.engine.replace_mode_after_keyword(input_list, keyword, replacement)
        self.assertEqual(output, expected_output)

        # Case 3: Keyword does not exist
        input_list = ["Line 1", "Line 2", "Line 3"]
        expected_output = ["Line 1", "Line 2", "Line 3"]
        output = self.engine.replace_mode_after_keyword(input_list, keyword, replacement)
        self.assertEqual(output, expected_output)

        # Case 4: Empty input list
        input_list = []
        expected_output = []
        output = self.engine.replace_mode_after_keyword(input_list, keyword, replacement)
        self.assertEqual(output, expected_output)

    def test_adjust_feeds_and_speeds(self):
        # Case 1: Upper case, float spindle speed
        gcode_lines = [
            "G1 X10 Y10 F100",
            "G1 Z-5 F200",
            "G1 X30 Y30 Z-2",
            "S1000.0"
        ]

        feedrate = 150
        plungerate = 250
        spindle_speed = 5000

        expected_output = [
            "G1 X10 Y10 F150",
            "G1 Z-5 F250",
            "G1 X30 Y30 Z-2",
            "S5000"
        ]

        output = self.engine.adjust_feeds_and_speeds(gcode_lines, feedrate, plungerate, spindle_speed)
        self.assertEqual(output, expected_output)

        # Case 2: Lower case, integer spindle speed
        gcode_lines = [
            "g1 x10 y10 f100",
            "g1 z-5 f200",
            "g1 x30 y30 z-2",
            "s1000"
        ]

        feedrate = 150
        plungerate = 250
        spindle_speed = 5000

        expected_output = [
            "G1 X10 Y10 F150",
            "G1 Z-5 F250",
            "G1 X30 Y30 Z-2",
            "S5000"
        ]

        output = self.engine.adjust_feeds_and_speeds(gcode_lines, feedrate, plungerate, spindle_speed)
        self.assertEqual(output, expected_output)

    def test_extract_cut_depth_and_z_safe_distance(self):
        # Case 1: Both cut depth and z safe distance are present in the gcode lines
        gcode_lines = [
            "(Cut depth: -12.000)",
            "(Z safe distance: 5.080)",
            "(Final part x dim: 1250.0)",
            "(Final part y dim: 640.0)",
            "",
            "(VECTRIC POST REVISION)",
            "(B467C182A25E2781624BDAEC17A0D7CE)",
            "T1",
            "G17",
            "G21",
            "G90",
            "G0Z20.320",
            "G0X0.000Y0.000",
            "S20000M3",
            "G0X348.294Y189.894Z5.080",
            "G1Z-12.000F750.0",
            "G1X348.249Y189.981F3000.0",
            "G1X348.209Y190.071",
            "G1X348.173Y190.163"
        ]

        expected_output = ("-12.000", "5.080")
        output = self.engine.extract_cut_depth_and_z_safe_distance(gcode_lines)
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

    def test_apply_datum_offset(self):
        # Case 1: No adjustment needed
        gcode_lines = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        x_adjustment = 0
        y_adjustment = 0
        expected_output = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        output = self.engine.apply_datum_offset(gcode_lines, x_adjustment, y_adjustment)
        self.assertEqual(output, expected_output)

        # Case 2: Positive adjustment
        gcode_lines = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        x_adjustment = 5
        y_adjustment = 10
        expected_output = ["G1 X15 Y30", "G1 Z5", "G1 X35 Y50"]
        output = self.engine.apply_datum_offset(gcode_lines, x_adjustment, y_adjustment)
        self.assertEqual(output, expected_output)

        # Case 3: Negative adjustment
        gcode_lines = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        x_adjustment = -5
        y_adjustment = -10
        expected_output = ["G1 X5 Y10", "G1 Z5", "G1 X25 Y30"]
        output = self.engine.apply_datum_offset(gcode_lines, x_adjustment, y_adjustment)
        self.assertEqual(output, expected_output)

        # Case 4: Mixed positive and negative adjustment
        gcode_lines = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        x_adjustment = 2
        y_adjustment = -8
        expected_output = ["G1 X12 Y12", "G1 Z5", "G1 X32 Y32"]
        output = self.engine.apply_datum_offset(gcode_lines, x_adjustment, y_adjustment)
        self.assertEqual(output, expected_output)

        # Case 5: No adjustment needed for Z axis
        gcode_lines = ["G1 X10 Y20", "G1 Z5", "G1 X30 Y40"]
        x_adjustment = 5
        y_adjustment = 10
        expected_output = ["G1 X15 Y30", "G1 Z5", "G1 X35 Y50"]
        output = self.engine.apply_datum_offset(gcode_lines, x_adjustment, y_adjustment)
        self.assertEqual(output, expected_output)

    def test_format_float_integer(self):
        # Case 1: Integer value
        value = 10
        expected_output = "10"
        output = self.engine.format_float(value)
        self.assertEqual(output, expected_output)

        # Case 2: Negative integer value
        value = -5
        expected_output = "-5"
        output = self.engine.format_float(value)
        self.assertEqual(output, expected_output)

        # Case 3: Decimal value without extra zeros
        value = 3.14
        expected_output = "3.14"
        output = self.engine.format_float(value)
        self.assertEqual(output, expected_output)

        # Case 4: Decimal value with extra zeros
        value = 2.5000
        expected_output = "2.5"
        output = self.engine.format_float(value)
        self.assertEqual(output, expected_output)

        # Case 5: Negative decimal value
        value = -1.234
        expected_output = "-1.234"
        output = self.engine.format_float(value)
        self.assertEqual(output, expected_output)

    def test_repeat_for_depths(self):
        # Case 1: Single pass depth
        gcode_lines = [
            "G1 X0 Y0 Z[cut depth]",
            "G1 X10 Y10 Z[cut depth]",
            "G1 X20 Y20 Z[cut depth]",
            "G1 X30 Y30 Z[cut depth]",
            "G1 X40 Y40 Z[cut depth]",
        ]
        pass_depths = [5]
        start_line_key = 0
        end_line_key = 5
        expected_output = [
                "G1 X0 Y0 Z-5",
                "G1 X10 Y10 Z-5",
                "G1 X20 Y20 Z-5",
                "G1 X30 Y30 Z-5",
                "G1 X40 Y40 Z-5",
        ]
        output = self.engine.repeat_for_depths(gcode_lines, pass_depths, start_line_key, end_line_key)
        self.assertEqual(output, expected_output)

        # Case 2: Multiple pass depths
        gcode_lines = [
            "G1 X0 Y0 Z[cut depth]",
            "G1 X10 Y10 Z[cut depth]",
            "G1 X20 Y20 Z[cut depth]",
            "G1 X30 Y30 Z[cut depth]",
            "G1 X40 Y40 Z[cut depth]",
        ]
        pass_depths = [5, 10, 15]
        start_line_key = 0
        end_line_key = 5
        expected_output = [
                "G1 X0 Y0 Z-5",
                "G1 X10 Y10 Z-5",
                "G1 X20 Y20 Z-5",
                "G1 X30 Y30 Z-5",
                "G1 X40 Y40 Z-5",
                "G1 X0 Y0 Z-10",
                "G1 X10 Y10 Z-10",
                "G1 X20 Y20 Z-10",
                "G1 X30 Y30 Z-10",
                "G1 X40 Y40 Z-10",
                "G1 X0 Y0 Z-15",
                "G1 X10 Y10 Z-15",
                "G1 X20 Y20 Z-15",
                "G1 X30 Y30 Z-15",
                "G1 X40 Y40 Z-15",
        ]
        output = self.engine.repeat_for_depths(gcode_lines, pass_depths, start_line_key, end_line_key)
        self.assertEqual(output, expected_output)

    def test_add_partoff(self):
        # Test case 1: Insert partoff line at the beginning of the gcode
        gcode_lines = ["G1 X10 Y20", "G1 X30 Y40"]
        processing_args = {
            "insertion_key": "G1 X10 Y20",
            "start_coordinate": (0, 0),
            "end_coordinate": (50, 50),
            "pass_depths": [5, 10],
            "feedrate": 100,
            "plungerate": 50,
            "z_safe_distance": 2
        }
        expected_output = [
            "(Partoff)",
            "G1 Z2",
            "G0 X0 Y0F100",
            "G1 Z-5 F50",
            "G1 X50 Y50F100",
            "G1 Z-10 F50",
            "G1 X0 Y0F100",
            "G1 Z2",
            "G1 X10 Y20",
            "G1 X30 Y40"
        ]
        output = self.engine.add_partoff(gcode_lines, **processing_args)
        self.assertEqual(output, expected_output)

        # Test case 2: Insert partoff line in the middle of the gcode
        gcode_lines = ["G1 X10 Y20", "G1 X30 Y40", "G1 X50 Y60"]
        processing_args = {
            "insertion_key": "G1 X30 Y40",
            "start_coordinate": (20, 20),
            "end_coordinate": (40, 40),
            "pass_depths": [5, 10, 15],
            "feedrate": 200,
            "plungerate": 100,
            "z_safe_distance": 3
        }
        expected_output = [
            "G1 X10 Y20",
            "(Partoff)",
            "G1 Z3",
            "G0 X20 Y20F200",
            "G1 Z-5 F100",
            "G1 X40 Y40F200",
            "G1 Z-10 F100",
            "G1 X20 Y20F200",
            "G1 Z-15 F100",
            "G1 X40 Y40F200",
            "G1 Z3",
            "G1 X30 Y40",
            "G1 X50 Y60"
        ]
        output = self.engine.add_partoff(gcode_lines, **processing_args)
        self.assertEqual(output, expected_output)

        # Test case 3: Insert partoff line at the end of the gcode
        gcode_lines = ["G1 X10 Y20", "G1 X30 Y40", "G1 X50 Y60"]
        processing_args = {
            "insertion_key": "G1 X50 Y60",
            "start_coordinate": (40, 40),
            "end_coordinate": (60, 60),
            "pass_depths": [5, 10, 15, 20],
            "feedrate": 300,
            "plungerate": 150,
            "z_safe_distance": 4
        }
        expected_output = [
            "G1 X10 Y20",
            "G1 X30 Y40",
            "(Partoff)",
            "G1 Z4",
            "G0 X40 Y40F300",
            "G1 Z-5 F150",
            "G1 X60 Y60F300",
            "G1 Z-10 F150",
            "G1 X40 Y40F300",
            "G1 Z-15 F150",
            "G1 X60 Y60F300",
            "G1 Z-20 F150",
            "G1 X40 Y40F300",
            "G1 Z4",
            "G1 X50 Y60"
        ]
        output = self.engine.add_partoff(gcode_lines, **processing_args)
        self.assertEqual(output, expected_output)

    def test_read_in_custom_shape_dimensions(self):
        # Case 1: All dimensions present
        gcode_lines = [
            "Line 1",
            "(Final part x dim: 10.5)",
            "(Final part y dim: 20.3)",
            "(x min: 0.0)", 
            "(y min: 0.0)",
            "Line 4"
        ]
        expected_output = ("10.5", "20.3", "0.0", "0.0")
        output = self.engine.read_in_custom_shape_dimensions(gcode_lines)
        self.assertEqual(output, expected_output)

        # Case 2: All values found on the same line
        gcode_lines = [
            "Line 1",
            "(Final part x dim: 10.5, Final part y dim: 20.3, x min: 0.0, y min: 0.0)",
            "Line 3",
            "Line 4"
        ]
        expected_output = ("10.5", "20.3", "0.0", "0.0")
        output = self.engine.read_in_custom_shape_dimensions(gcode_lines)
        self.assertEqual(output, expected_output)

    def test_get_custom_shape_extents(self):
        # Case 1: Custom shape type is defined
        self.engine.config.active_config.shape_type = "custom_shape"
        self.engine.custom_gcode_shapes = ["custom_shape"]
        self.engine.source_folder_path = "/path/to/gcode/files"
        self.engine.config.active_cutter.dimensions.tool_diameter = 10

        # Mocking the return values of helper methods
        self.engine.find_and_read_gcode_file = lambda path, shape_type, diameter: ["G1 X10 Y20", "G1 X30 Y40"]
        self.engine.read_in_custom_shape_dimensions = lambda lines: ("40", "60", "10", "20")

        expected_output = (40.0, 60.0, 10.0, 20.0)
        output = self.engine.get_custom_shape_extents()
        self.assertEqual(output, expected_output)

        # Case 2: Custom shape type is not defined
        self.engine.config.active_config.shape_type = "invalid_shape"
        self.engine.custom_gcode_shapes = ["custom_shape"]

        with self.assertRaises(Exception):
            self.engine.get_custom_shape_extents()

if __name__ == '__main__':
    unittest.main()