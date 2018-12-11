from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.clock import Clock
from kivy.graphics import *
from kivy.utils import *
import math
from datetime import datetime
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout



Builder.load_string("""

<GCodeView>:

    gCodePreview:gCodePreview

    StencilBox:
        size: self.parent.size
        pos: self.parent.pos
        Scatter:
#             canvas.after:
#                 Color:
#                     rgba: 1,0,0,.5
#                 Rectangle:
#                     size: self.size
#                     pos: self.pos
            id: gCodePreview
#             center: self.parent.center
#             size: self.parent.size
            do_rotation: False
            do_translation: True
            do_scale: True



""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


class StencilBox(StencilView, BoxLayout):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_up(touch)


class GCodeView(Widget):

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0

    g0_move_colour = get_color_from_hex('#f4433655')
    feed_move_colour = get_color_from_hex('#2196f355')
    line_width = 1

#     def __init__(self, **kwargs):
#         super(GCodeView, self).__init__(**kwargs)


    def draw_file_in_xy_plane(self, gcode_list):
        log('len(gcode_list) ' + str(len(gcode_list)))
        self.gCodePreview.canvas.clear()
#        log('> set_canvas_scale')
        self.set_canvas_scale(gcode_list)
#        log('< set_canvas_scale')

        last_x, last_y = 0, 0
        target_x, target_y = 0, 0

        plane = 'G17'
        move = 'G0'
        lines_read = 0
        max_lines_to_read = 1000

        log('> for line in gcode_list')
        for line in gcode_list:

            lines_read += 1
            if lines_read > 1000: break

            for bit in line.split(' '):
                # find plane
                if bit == 'G17': plane = 'G17' # 'xy'
                elif bit == 'G18': plane = 'G18' # 'zx'
                elif bit == 'G19': plane = 'G19' # 'yz'
                # else plane remains same as last loop

                # find move
                elif bit == 'G0': move = 'G0' # Fast move, straight
                elif bit == 'G1': move = 'G1' # Feed move, straight
                elif bit == 'G2': move = 'G2' # CW arc
                elif bit == 'G3': move = 'G3' # CCW arc
                # else move remains same as last loop

            if plane == 'G17':

                if move == 'G0':
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'): target_x = float(bit[1:])
                        elif bit.startswith('Y'):
                            target_y = float(bit[1:])
                            break
                    with self.gCodePreview.canvas:
                        Color(self.g0_move_colour[0],self.g0_move_colour[1],self.g0_move_colour[2],self.g0_move_colour[3])
                        Line(points = [last_x, last_y, target_x, target_y],
                             close=False,
                             width=self.line_width)
                    last_x, last_y = target_x, target_y

                elif move == 'G1':
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'): target_x = float(bit[1:])
                        elif bit.startswith('Y'):
                            target_y = float(bit[1:])
                            break
                    with self.gCodePreview.canvas:
                        Color(self.feed_move_colour[0],self.feed_move_colour[1],self.feed_move_colour[2],self.feed_move_colour[3])
                        Line(points = [last_x, last_y, target_x, target_y],
                             close=False,
                             width=self.line_width)
                    last_x, last_y = target_x, target_y

                elif move == 'G2' or move == 'G3':

                    i, j = 0, 0 # resets each time'
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'): target_x = float(bit[1:])
                        elif bit.startswith('Y'): target_y = float(bit[1:])
                        elif bit.startswith('I'): i = float(bit[1:])
                        elif bit.startswith('J'):
                            j = float(bit[1:])
                            break

                    radius = round(math.sqrt(i**2+j**2),4)
                    start_quad = self.detect_quad_in_xy_plane(i, j)
                    end_i = (last_x + i) - target_x
                    end_j = (last_y + j) - target_y
                    end_quad = self.detect_quad_in_xy_plane(end_i, end_j)

                    if start_quad == 0.5: angle_start = 90
                    if start_quad == 1.5: angle_start = 0
                    if start_quad == 2.5: angle_start = 270
                    if start_quad == 3.5: angle_start = 180

                    if end_quad == 0.5: angle_end = 90
                    if end_quad == 1.5: angle_end = 0
                    if end_quad == 2.5: angle_end = 270
                    if end_quad == 3.5: angle_end = 180

                    if start_quad == 1: angle_start = math.degrees(math.acos(math.fabs(j)/radius))
                    if start_quad == 2: angle_start = math.degrees(math.acos(math.fabs(i)/radius)) + 270
                    if start_quad == 3: angle_start = math.degrees(math.acos(math.fabs(j)/radius)) + 180
                    if start_quad == 4: angle_start = math.degrees(math.acos(math.fabs(i)/radius)) + 90

                    if end_quad == 1: angle_end = math.degrees(math.acos(math.fabs(j)/radius))
                    if end_quad == 2: angle_end = math.degrees(math.acos(math.fabs(i)/radius)) + 270
                    if end_quad == 3: angle_end = math.degrees(math.acos(math.fabs(j)/radius)) + 180
                    if end_quad == 4: angle_end = math.degrees(math.acos(math.fabs(i)/radius)) + 90

                    # Kivy arcs drawn in direction of lowest angle to highest angle. For arcs passing thru zero degrees (@12 o'#clock pos), the end angle needs to be corrected in some cases. E.g. for CW, 270 -> 90 goes to 270 -> 360 +90 (450)
                    if move == 'G2' and angle_start > angle_end:
                        angle_end = angle_end + 360
                    if move == 'G3' and angle_start < angle_end:
                        angle_end = angle_end - 360

                    with self.gCodePreview.canvas:
                        # (center_x, center_y, radius, angle_start, angle_end, segments)
                        Color(self.feed_move_colour[0],self.feed_move_colour[1],self.feed_move_colour[2],self.feed_move_colour[3])
                        Line(circle=(last_x + i, last_y + j, radius, int(angle_start), int(angle_end), 10),
                             close=False,
                             width=self.line_width)
                    last_x, last_y = target_x, target_y

                else:
                    print 'Did not draw: ' + line
        log('< for line in gcode_list')


    def detect_quad_in_xy_plane(self,i,j):
        # quads defined mathematically, i.e. starting top right, counting ccw    .5 represents boundary between <round up/down> quadrants
        if i > 0:
            if j > 0: return 3
            if j < 0: return 2
            if j == 0: return 2.5
        elif i < 0:
            if j > 0: return 4
            if j < 0: return 1
            if j == 0: return 0.5
        elif i == 0:
            if j > 0: return 3.5
            if j < 0: return 1.5


    def set_canvas_scale(self, gcode_list):
#        x = []
#        y = []
#        max_x = 0
#        max_y = 0

        # find max values of X & Y to establish scale
#        for line in gcode_list:
#            for bit in line.strip().split(" "):
#                if bit.startswith('X'):
#                    x.append(float(bit[1:]))
#                elif bit.startswith('Y'):
#                    y.append(float(bit[1:]))
#                    break

#         scale_x = 700/max(x)
#         scale_y = 400/max(y)
#        scale_x = self.gCodePreview.size[0]/max(x)
#        scale_y = self.gCodePreview.size[1]/max(y)
        scale_x = self.gCodePreview.size[0] / float(self.max_x)
        scale_y = self.gCodePreview.size[1] / float(self.max_y)
        scale = min(scale_x, scale_y) * 0.9

        # setup canvas for drawing
        with self.gCodePreview.canvas:
            Scale(scale, scale, 1)
            Color(0, 1, 0, 1)


    def get_non_modal_gcode(self, file_to_draw):

        original_gcode = []
        xy_preview_gcode = []

        # load and clean file into list
        log('> get_non_modal_gcode: append loop')
        original_file = open(file_to_draw, 'r')
        for line in original_file:
            original_gcode.append(line.strip())
        original_file.close()
        log('< get_non_modal_gcode: append loop')

        self.min_x = 999999
        self.max_x = -999999
        self.min_y = 999999
        self.max_y = -999999
        self.min_z = 999999
        self.max_z = -999999

        # mode defaults
        last_x, last_y, last_z = '0', '0', '0'
        plane = 'G17'
        move = '0'
        feed_rate = 0
        line_number = 0
        log('> get_non_modal_gcode: process loop')
        for line in original_gcode:

            line_number += 1

            # centers reset each loop
            i, j, k = '0', '0', '0'

            if line.startswith('(') == True: continue   # skip any lines with comments
            elif len(line) <= 1: continue
            elif line.startswith('G') == True:
                # find move
                if line.startswith('G2 '): move = 'G2' # CW arc
                elif line.startswith('G3 '): move = 'G3' # CCW arc
                elif line.startswith('G0 '): move = 'G0' # Fast move, straight
                elif line.startswith('G1 '): move = 'G1' # Feed move, straight

                # find plane
                elif line.startswith('G17'): plane = 'G17' # 'xy'
                elif line.startswith('G18'): plane = 'G18' # 'zx'
                elif line.startswith('G19'): plane = 'G19' # 'yz'

            # Check every position for position information
            for bit in line.split(' '):
                start = bit[0]
                if start == 'X':
                    last_x = float(bit[1:])
                    if last_x > self.max_x: self.max_x = last_x
                    if last_x < self.min_x: self.min_x = last_x
                    last_x = bit[1:]
                elif start == 'Y':
                    last_y = float(bit[1:])
                    if last_y > self.max_y: self.max_y = last_y
                    if last_y < self.min_y: self.min_y = last_y
                    last_y = bit[1:]
                elif start == 'Z':
                    last_z = float(bit[1:])
                    if last_z > self.max_z: self.max_z = last_z
                    if last_z < self.min_z: self.min_z = last_z
                    last_z = bit[1:]
                elif start == 'F': feed_rate = bit[1:]
                elif start == 'I': i = bit[1:]
                elif start == 'J': j = bit[1:]
                elif start == 'K': k = bit[1:]

            if move == 'G0':
                processed_line = plane+' '+move+' X'+last_x+' Y'+last_y+' Z'+last_z
                xy_preview_gcode.append(processed_line)
            elif move == 'G1':
                processed_line = plane+' '+move+' X'+last_x+' Y'+last_y+' Z'+last_z+' F'+feed_rate
                xy_preview_gcode.append(processed_line)
            elif move == 'G2' or move == 'G3':
                processed_line = plane+' '+move+' X'+last_x+' Y'+last_y+' Z'+last_z+' I'+i+' J'+j+' K'+k+' F'+feed_rate
                xy_preview_gcode.append(processed_line)
            else: print 'Line not for preview ('+str(line_number)+move+'): ' + line

        log('< get_non_modal_gcode: process loop')
        return xy_preview_gcode
