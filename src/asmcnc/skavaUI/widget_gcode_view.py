from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics import *
from kivy.utils import *
import math
from datetime import datetime
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
import re
from functools import partial
Builder.load_string(
    """

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
"""
    )


def log(message):
    timestamp = datetime.now()
    print(timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + message)


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
    max_lines_to_read = 2000

    def __init__(self, **kwargs):
        super(GCodeView, self).__init__(**kwargs)
        self.jd = kwargs['job']

    def draw_file_in_xy_plane(self, gcode_list):
        self.gCodePreview.canvas.clear()
        self.set_canvas_scale(gcode_list)
        last_x, last_y = 0, 0
        target_x, target_y = 0, 0
        plane = 'G17'
        move = 'G0'
        lines_read = 0
        log('> for line in gcode_list')
        for line in gcode_list:
            lines_read += 1
            if lines_read > self.max_lines_to_read:
                break
            for bit in line.split(' '):
                if bit == 'G17':
                    plane = 'G17'
                elif bit == 'G18':
                    plane = 'G18'
                elif bit == 'G19':
                    plane = 'G19'
                elif bit == 'G0':
                    move = 'G0'
                elif bit == 'G1':
                    move = 'G1'
                elif bit == 'G2':
                    move = 'G2'
                elif bit == 'G3':
                    move = 'G3'
            if plane == 'G17':
                if move == 'G0':
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'):
                            target_x = float(bit[1:])
                        elif bit.startswith('Y'):
                            target_y = float(bit[1:])
                            break
                    with self.gCodePreview.canvas:
                        Color(self.g0_move_colour[0], self.g0_move_colour[1
                            ], self.g0_move_colour[2], self.g0_move_colour[3])
                        Line(points=[last_x, last_y, target_x, target_y],
                            close=False, width=self.line_width)
                    last_x, last_y = target_x, target_y
                elif move == 'G1':
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'):
                            target_x = float(bit[1:])
                        elif bit.startswith('Y'):
                            target_y = float(bit[1:])
                            break
                    with self.gCodePreview.canvas:
                        Color(self.feed_move_colour[0], self.
                            feed_move_colour[1], self.feed_move_colour[2],
                            self.feed_move_colour[3])
                        Line(points=[last_x, last_y, target_x, target_y],
                            close=False, width=self.line_width)
                    last_x, last_y = target_x, target_y
                elif move == 'G2' or move == 'G3':
                    i, j = 0, 0
                    for bit in line.strip().split(' '):
                        if bit.startswith('X'):
                            target_x = float(bit[1:])
                        elif bit.startswith('Y'):
                            target_y = float(bit[1:])
                        elif bit.startswith('I'):
                            i = float(bit[1:])
                        elif bit.startswith('J'):
                            j = float(bit[1:])
                            break
                    radius = round(math.sqrt(i ** 2 + j ** 2), 4)
                    start_quad = self.detect_quad_in_xy_plane(i, j)
                    end_i = last_x + i - target_x
                    end_j = last_y + j - target_y
                    end_quad = self.detect_quad_in_xy_plane(end_i, end_j)
                    if start_quad == 0.5:
                        angle_start = 90
                    if start_quad == 1.5:
                        angle_start = 0
                    if start_quad == 2.5:
                        angle_start = 270
                    if start_quad == 3.5:
                        angle_start = 180
                    if end_quad == 0.5:
                        angle_end = 90
                    if end_quad == 1.5:
                        angle_end = 0
                    if end_quad == 2.5:
                        angle_end = 270
                    if end_quad == 3.5:
                        angle_end = 180
                    if start_quad == 1:
                        angle_start = math.degrees(math.acos(math.fabs(j) /
                            radius))
                    if start_quad == 2:
                        angle_start = math.degrees(math.acos(math.fabs(i) /
                            radius)) + 270
                    if start_quad == 3:
                        angle_start = math.degrees(math.acos(math.fabs(j) /
                            radius)) + 180
                    if start_quad == 4:
                        angle_start = math.degrees(math.acos(math.fabs(i) /
                            radius)) + 90
                    if end_quad == 1:
                        angle_end = math.degrees(math.acos(math.fabs(j) /
                            radius))
                    if end_quad == 2:
                        angle_end = math.degrees(math.acos(math.fabs(i) /
                            radius)) + 270
                    if end_quad == 3:
                        angle_end = math.degrees(math.acos(math.fabs(j) /
                            radius)) + 180
                    if end_quad == 4:
                        angle_end = math.degrees(math.acos(math.fabs(i) /
                            radius)) + 90
                    if move == 'G2' and angle_start > angle_end:
                        angle_end = angle_end + 360
                    if move == 'G3' and angle_start < angle_end:
                        angle_end = angle_end - 360
                    with self.gCodePreview.canvas:
                        Color(self.feed_move_colour[0], self.
                            feed_move_colour[1], self.feed_move_colour[2],
                            self.feed_move_colour[3])
                        Line(circle=(last_x + i, last_y + j, radius, int(
                            angle_start), int(angle_end), 10), close=False,
                            width=self.line_width)
                    last_x, last_y = target_x, target_y
                else:
                    print('Did not draw: ' + line)
        log('< for line in gcode_list')

    def detect_quad_in_xy_plane(self, i, j):
        if i > 0:
            if j > 0:
                return 3
            if j < 0:
                return 2
            if j == 0:
                return 2.5
        elif i < 0:
            if j > 0:
                return 4
            if j < 0:
                return 1
            if j == 0:
                return 0.5
        elif i == 0:
            if j > 0:
                return 3.5
            if j < 0:
                return 1.5

    def set_canvas_scale(self, gcode_list):
        scale_x = self.gCodePreview.size[0] / float(self.max_x)
        scale_y = self.gCodePreview.size[1] / float(self.max_y)
        scale = min(scale_x, scale_y) * 0.9
        with self.gCodePreview.canvas:
            Scale(scale, scale, 1)
            Color(0, 1, 0, 1)
    interrupt_line_threshold = 5000
    interrupt_delay = 0.2

    def prep_for_non_modal_gcode(self, job_file_gcode, line_cap,
        screen_manager, dt):
        self.line_number = 0
        self.lines_read = 0
        self.line_threshold_to_pause_and_update_at = (self.
            interrupt_line_threshold)
        self.total_lines_in_job_file_pre_scrubbed = len(job_file_gcode)
        self.min_x = 999999
        self.max_x = -999999
        self.min_y = 999999
        self.max_y = -999999
        self.min_z = 999999
        self.max_z = -999999
        self.last_x, self.last_y, self.last_z = '0', '0', '0'
        self.plane = 'G17'
        self.move = '0'
        self.feed_rate = 0
        self.feed_rate_list = []
        self.speed_list = []
        self.xy_preview_gcode = []
        log('> Getting non modal gcode: process loop...')
        self.get_non_modal_gcode(job_file_gcode, line_cap, screen_manager, dt)

    def get_non_modal_gcode(self, job_file_gcode, line_cap, screen_manager, dt
        ):
        if self.lines_read < self.total_lines_in_job_file_pre_scrubbed:
            break_threshold = min(self.
                line_threshold_to_pause_and_update_at, self.
                total_lines_in_job_file_pre_scrubbed)
            while self.lines_read < break_threshold:
                draw_line = job_file_gcode[self.lines_read]
                self.lines_read += 1
                if (line_cap == True and self.lines_read > self.
                    max_lines_to_read):
                    break
                line = draw_line
                line = re.sub('Y', ' YY', line)
                line = re.sub('X', ' XX', line)
                line = re.sub('Z', ' ZZ', line)
                line = re.sub('F', ' FF', line)
                line = re.sub('S', ' SS', line)
                line = re.sub('I', ' II', line)
                line = re.sub('J', ' JJ', line)
                line = re.sub('K', ' KK', line)
                line = re.sub('G', ' GG', line)
                self.line_number += 1
                i, j, k = '0', '0', '0'
                if line.startswith('(') == True:
                    continue
                elif len(line) <= 1:
                    continue
                for idx, bit in enumerate(re.split(
                    '( X| Y| Z| F| S| I| J| K| G)', line)):
                    if bit == '':
                        continue
                    if idx == 2:
                        if bit == 'G2':
                            self.move = 'G2'
                        elif bit == 'G3':
                            self.move = 'G3'
                        elif bit == 'G0':
                            self.move = 'G0'
                        elif bit == 'G1':
                            self.move = 'G1'
                        elif bit == 'G17':
                            self.plane = 'G17'
                        elif bit == 'G18':
                            self.plane = 'G18'
                        elif bit == 'G19':
                            self.plane = 'G19'
                    start = bit[0]
                    if start == 'X':
                        try:
                            self.last_x = float(bit[1:])
                            if self.last_x > self.max_x:
                                self.max_x = self.last_x
                            if self.last_x < self.min_x:
                                self.min_x = self.last_x
                            self.last_x = bit[1:]
                        except:
                            print('Line not for preview (' + str(self.
                                line_number) + '): ' + line)
                    elif start == 'Y':
                        try:
                            self.last_y = float(bit[1:])
                            if self.last_y > self.max_y:
                                self.max_y = self.last_y
                            if self.last_y < self.min_y:
                                self.min_y = self.last_y
                            self.last_y = bit[1:]
                        except:
                            print('Line not for preview (' + str(self.
                                line_number) + '): ' + line)
                    elif start == 'Z':
                        try:
                            self.last_z = float(bit[1:])
                            if self.last_z > self.max_z:
                                self.max_z = self.last_z
                            if self.last_z < self.min_z:
                                self.min_z = self.last_z
                            self.last_z = bit[1:]
                        except:
                            print('Line not for preview (' + str(self.
                                line_number) + '): ' + line)
                    elif start == 'F':
                        self.feed_rate = bit[1:]
                    elif start == 'I':
                        i = bit[1:]
                    elif start == 'J':
                        j = bit[1:]
                    elif start == 'K':
                        k = bit[1:]
                if self.move == 'G0':
                    processed_line = (self.plane + ' ' + self.move + ' X' +
                        self.last_x + ' Y' + self.last_y + ' Z' + self.last_z)
                    self.xy_preview_gcode.append(processed_line)
                elif self.move == 'G1':
                    processed_line = (self.plane + ' ' + self.move + ' X' +
                        self.last_x + ' Y' + self.last_y + ' Z' + self.
                        last_z + ' F' + self.feed_rate)
                    self.xy_preview_gcode.append(processed_line)
                elif self.move == 'G2' or self.move == 'G3':
                    processed_line = (self.plane + ' ' + self.move + ' X' +
                        self.last_x + ' Y' + self.last_y + ' Z' + self.
                        last_z + ' I' + i + ' J' + j + ' K' + k + ' F' +
                        self.feed_rate)
                    self.xy_preview_gcode.append(processed_line)
                else:
                    print('Line not for preview (' + str(self.line_number
                        ) + self.move + '): ' + line)
            self.line_threshold_to_pause_and_update_at += (self.
                interrupt_line_threshold)
            percentage_progress = int(self.lines_read * 1.0 / self.
                total_lines_in_job_file_pre_scrubbed * 1.0 * 100.0)
            screen_manager.get_screen('loading').update_screen('Analysing',
                percentage_progress)
            Clock.schedule_once(partial(self.get_non_modal_gcode,
                job_file_gcode, line_cap, screen_manager), self.interrupt_delay
                )
        else:
            log('> Finished getting non modal gcode')
            self.jd.x_max = self.max_x
            self.jd.x_min = self.min_x
            self.jd.y_max = self.max_y
            self.jd.y_min = self.min_y
            self.jd.z_max = self.max_z
            self.jd.z_min = self.min_z
            screen_manager.get_screen('loading')._finish_loading(self.
                xy_preview_gcode)
