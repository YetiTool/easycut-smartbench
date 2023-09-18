from curses.textpad import rectangle
import os, sys, subprocess
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

import svgwrite
from svgpathtools import svg2paths, parse_path

Builder.load_string("""
<GeberitCutterScreen>:

    editor_container:editor_container

    filename_input:filename_input
    feed_input:feed_input
    speed_input:speed_input
    depth_input:depth_input
    shape_label:shape_label
                    
    add_shape_button:add_shape_button
    add_shape_button_image:add_shape_button_image

    BoxLayout:
        orientation: 'horizontal'

        canvas.before:
            Color:
                rgba: hex('#E2E2E2FF')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_x: 0.3
            orientation: 'vertical'
            padding: dp(10)
                    
            Label:
                size_hint_y: 0.3
                text: 'Shape cutter'
                color: 0,0,0,1
                font_size: dp(24)

            BoxLayout:
                size_hint_y: 1.3

                Button:
                    id: add_shape_button
                    background_color: [0,0,0,0]
                    on_press: root.add_shape()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: add_shape_button_image
                            source: "./asmcnc/apps/geberit_cutter_app/img/rectangle_shape_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                    
            GridLayout:
                cols: 1
                rows: 2
                
                Label:
                    size_hint_y: 0.3
                    text: 'Draw:'
                    color: 0,0,0,1
                    font_size: dp(20)  

                Label:
                    id: shape_label
                    size_hint_y: 0.3
                    text: 'Rectangle'
                    color: 0,0,0,1
                    font_size: dp(20)  

            BoxLayout:
                    
                Button:
                    background_color: [0,0,0,0]
                    on_press: root.toggle_change_shape()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/geberit_cutter_app/img/shape_toggle_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                    
                Button:
                    background_color: [0,0,0,0]
                    on_press: root.rotate_shape()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/geberit_cutter_app/img/rotate_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                    
            BoxLayout:

                Button:
                    background_color: [0,0,0,0]
                    on_press: root.save()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/save_button_132.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                    
                Button:
                    background_color: [0,0,0,0]
                    on_press: root.clear_all()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/geberit_cutter_app/img/clear_all_button.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                size_hint_y: 0.28
                orientation: 'horizontal'

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(10)
                    padding: [dp(10), dp(10), dp(10), dp(0)]

                    # BoxLayout:
                    #     orientation: 'horizontal'
                    #     spacing: dp(10)

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock length'
                    #         input_filter: 'int'
                    #         disabled: True

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock width'
                    #         input_filter: 'int'
                    #         disabled: True

                    #     TextInput:
                    #         font_size: dp(20)
                    #         multiline: False
                    #         hint_text: 'Stock depth'
                    #         input_filter: 'int'
                    #         disabled: True

                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)

                        TextInput:
                            id: feed_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Feed'
                            input_filter: 'int'

                        TextInput:
                            id: speed_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Speed'
                            input_filter: 'int'

                        TextInput:
                            id: depth_input
                            font_size: dp(20)
                            multiline: False
                            hint_text: 'Material thickness'
                            input_filter: 'int'

                        # TextInput:
                        #     font_size: dp(20)
                        #     multiline: False
                        #     hint_text: '# of passes'
                        #     input_filter: 'int'

                    TextInput:
                        id: filename_input
                        font_size: dp(20)
                        multiline: False
                        text: 'rectangle.gcode'
                        hint_text: 'Enter filename'                        
                    
                    Label:
                        size_hint_y: 0.3
                        text: 'Canvas'
                        color: 0,0,0,1
                        font_size: dp(20)

                Button:
                    size_hint_x: 0.2
                    background_color: [0,0,0,0]
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout:
                padding: [dp(5), dp((self.height - (self.width / 2)) / 2)]

                BoxLayout:
                    width: dp(600)
                    height: dp(300)
                    size_hint: (None, None)

                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: .5, .5, .5, 1
                            Line:
                                width: 2
                                rectangle: self.x, self.y, self.width, self.height

                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            Rectangle:
                                size: self.size
                                pos: self.pos

                        StencilView:
                            size: self.parent.size
                            pos: self.parent.pos

                            FloatLayout:
                                id: editor_container
                                size: self.parent.size
                                pos: self.parent.pos

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class shapeWidget(Scatter):

    shape_image_filepath = "./asmcnc/apps/geberit_cutter_app/img/geberit_panel.png"

    shape_selected_image_filepath = "./asmcnc/apps/geberit_cutter_app/img/geberit_panel_selected.png"

    shape_index = 0
    shape_type = "None" 

    def __init__(self, shape_height, pos, **kwargs):
        super(shapeWidget, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']

        shape_width = shape_height / 2
        self.size_hint = (None, None)
        self.size = (shape_width, shape_height)
        self.pos = pos
        self.do_rotation=False
        self.do_scale=False

        self.shape_image = Image(source=self.shape_image_filepath, size_hint=(None,None), size=(shape_width,shape_height))
        self.add_widget(self.shape_image)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.select_shape()

        return super(shapeWidget, self).on_touch_down(touch)

    def select_shape(self):
        # When clicked, show that the shape is selected by changing its colour
        current_shape_selection = self.sm.get_screen('geberit_cutter').current_shape_selection
        if current_shape_selection:
            current_shape_selection.shape_image.source = self.shape_image_filepath

        self.shape_image.source = self.shape_selected_image_filepath
        self.sm.get_screen('geberit_cutter').current_shape_selection = self

    def rotate_clockwise(self):
        self.rotation -= 90

class GeberitCutterScreen(Screen):

    svg_output_filepath = './asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg'
    raw_gcode_filepath = './asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc'

    shapes_added = 0
    current_shape_selection = None

    image_index = 0

    current_shape = 'RECTANGLE'
    max_shapes = 4

    z_lift_height = 5 #mm

    def __init__(self, **kwargs):
        super(GeberitCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

    def add_shape(self):
        print("add shape")
        print('shapes_added:', str(self.shapes_added))
        if self.shapes_added < self.max_shapes:
            print('Condition met')
            self.shapes_added += 1
            new_shape = shapeWidget(self.editor_container.height, self.editor_container.pos, screen_manager=self.sm)
            new_shape.shape_type = self.current_shape
            new_shape.shape_index = self.image_index
            print("Setting shape type to:", self.current_shape)
            new_shape.select_shape()
            self.editor_container.add_widget(new_shape)

    def cycle_button_image(self):
        image_sources = [
            "./asmcnc/apps/geberit_cutter_app/img/rectangle_shape_button.png",
            "./asmcnc/apps/geberit_cutter_app/img/circle_shape_button.png",
            "./asmcnc/apps/geberit_cutter_app/img/line_shape_button.png"
        ]
        self.shapes = [
            'Rectangle',
            'Circle',
            'Line'
        ]

        #Rotate list by 1 element (bug correction)
        if len(self.shapes) > 1:
            first_element = self.shapes.pop(0)  # Remove and store the first element
            self.shapes.append(first_element)  # Append the first element to the end

        button_image = self.add_shape_button_image
        current_image_source = button_image.source
        current_image_index = image_sources.index(current_image_source)
        current_shape = self.shapes[current_image_index]
        next_image_index = (current_image_index + 1) % len(image_sources)
        button_image.source = image_sources[next_image_index]

        if 'rectangle' in current_shape.lower():
            self.add_shape_button.disabled = False
            print("Button enabled")
        else:
            self.add_shape_button.disabled = True
            print("Button disabled")

        return current_shape, current_image_index
    

    def rotate_shape(self):
        if self.current_shape_selection:
            self.current_shape_selection.rotate_clockwise()

    def update_shape_label(self, shape):
        self.shape_label.text = shape

    def toggle_change_shape(self):
        self.current_shape, self.image_index = self.cycle_button_image()
        self.update_shape_label(self.current_shape)

    def clear_all(self):
        print("clear all")
        self.editor_container.clear_widgets()
        self.shapes_added = 0

    def save(self):
        if not (self.filename_input.text and self.feed_input.text and self.speed_input.text and self.depth_input.text):
            popup_info.PopupError(self.sm, self.l, "Please ensure that every text box is filled in.")
            return

        if self.filename_input.text.endswith(('.nc','.NC','.gcode','.GCODE','.GCode','.Gcode','.gCode')):
            self.wait_popup = popup_info.PopupWait(self.sm, self.l)
            Clock.schedule_once(lambda dt: self.convert_to_gcode(), 0.5)
        else:
            popup_info.PopupError(self.sm, self.l, "Please ensure that the filename ends with a valid GCode file extension.")

    def convert_to_gcode(self):
        def generate_svg():
            # Viewbox can be set to the container size, so that positions can then be defined in pixels rather than relative to actual size of the SVG
            # The height and width are switched - this is necessary so that everything is drawn in full size but out of bounds, which is fixed by a reflection further down
            dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('1200mm','2400mm'), viewBox='0 0 %s %s' % (self.editor_container.height, self.editor_container.width))
            for shape in self.editor_container.children:

                # Position has to be converted to local coordinates of the container, as they are relative to the window
                shape_pos = self.editor_container.to_local(shape.x, shape.y, relative=True)

                # The long side has to be drawn parallel to the y axis - to solve this, this matrix transformation performs a reflection in the line y=x
                # This means that the long side can be drawn parallel to the x axis, directly from the kivy coords, instead of figuring out how to switch all the x/y coords
                transformation = "matrix(0 1 1 0 0 0)"
                # Additionally, when a shape is drawn, a scaling and translation is applied, which vertically flips the svg
                # This is needed because kivy measures Y coords from the opposite end of the screen and draws stuff upside down
                transformation += " scale(1,-1) translate(0,%s)" % -self.editor_container.height

                # Now rotate around the centre of the shape, which again needs the coord converted
                shape_centre = self.editor_container.to_local(*shape.center, relative=True)
                # Then add rotation
                transformation += " rotate(%s,%s,%s)" % (shape.rotation, shape_centre[0], shape_centre[1])

                # If the shape is turned sideways
                if int(shape.rotation) % 180 != 0:
                    # Then rotation will mess up its position so align centre first
                    # It is important to note that this has to be added after the rotation, because transformations are performed right to left
                    transformation += " translate(%s,%s)" % (shape.width/2, -shape.height/4)

                shape_size = (shape.width, shape.height)

                shape_type = shape.shape_type

                print("shape.shape_type:", shape_type)

                if shape_type.lower() == "rectangle":
                    # Create rectangle 
                    dwg.add(dwg.rect(shape_pos, shape_size, fill='white', stroke='black', transform=transformation))
                elif shape_type.lower() == "circle":
                    # Create circle
                    circle_centre = (shape_pos[0] + (shape.width / 2), shape_pos[1] + (shape.height / 4))
                    circle_radius = shape.width / 2
                    dwg.add(dwg.circle(circle_centre, circle_radius, fill='white', stroke='black', transform=transformation))
                
                '''
                # Set up objects for the detail of the shape as relative to rectangle position and size
                # The same transform can be used as the rectangle transform as it is done relative to the centre of the shape
                big_circle_centre = (shape_pos[0] + (shape.width / 2), shape_pos[1] + (shape.height / 4))
                big_circle_radius = shape.height / 10
                dwg.add(dwg.circle(big_circle_centre, big_circle_radius, fill='white', stroke='black', transform=transformation))

                small_circle_centre = (shape_pos[0] + (shape.width / 2), shape_pos[1] + (shape.height * 0.45))
                small_circle_radius = shape.height / 40
                dwg.add(dwg.circle(small_circle_centre, small_circle_radius, fill='white', stroke='black', transform=transformation))

                small_rect_pos = (shape_pos[0] + (shape.width / 4), shape_pos[1] + (shape.height * 0.78))
                small_rect_size = (shape.width / 2, shape.width / 4)
                dwg.add(dwg.rect(small_rect_pos, small_rect_size, fill='white', stroke='black', transform=transformation))

                rounded_rect_size = (shape.width / 6, shape.width / 16)
                roundedness = rounded_rect_size[0] / 10

                rounded_rect_left_pos = (shape_pos[0] + (shape.width * 0.18), shape_pos[1] + (shape.height * 0.37))
                dwg.add(dwg.rect(rounded_rect_left_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))

                rounded_rect_right_pos = (shape_pos[0] + (shape.width * 0.82) - rounded_rect_size[0], shape_pos[1] + (shape.height * 0.37))
                dwg.add(dwg.rect(rounded_rect_right_pos, rounded_rect_size, roundedness, roundedness, fill='white', stroke='black', transform=transformation))
                '''
            dwg.save()

            convert_svg_to_paths()

        def convert_svg_to_paths():
            # The svg now has to be converted to paths, as required by the gcode converter
            paths, attributes = svg2paths(self.svg_output_filepath)
            dwg = svgwrite.Drawing(filename=self.svg_output_filepath, size=('1200mm','2400mm'), viewBox='0 0 %s %s' % (self.editor_container.height, self.editor_container.width))
            for i, path in enumerate(paths):
                # Recover attributes of current path, or else transformation is lost
                path_attributes = attributes[i]
                # Convert from svgpathtools path to svgwrite path using shared attribute d
                dwg.add(svgwrite.path.Path(path.d(), fill=path_attributes['fill'], stroke=path_attributes['stroke'], transform=path_attributes['transform']))
            dwg.save()

            convert_svg_to_gcode()

        def convert_svg_to_gcode():
            # Now, convert to gcode
            if sys.platform != "win32":
                cmd = "cargo run --release -- /home/pi/easycut-smartbench/src/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg"
                # As svg2gcode does not allow for spindle speed or depth to be set, both of those are included in the spindle on command
                cmd += " --off M5 --on M3S%sG1Z%sF%s --feedrate %s -o /home/pi/easycut-smartbench/src/asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc" % (self.speed_input.text, "-" + self.depth_input.text, self.feed_input.text, self.feed_input.text)
                working_directory = '/home/pi/svg2gcode'
            else:
                # For this to work on windows, cargo and svg2gcode need to be installed in the right places relative to easycut
                cmd = "%s/../../../.cargo/bin/cargo.exe run --release -- %s/asmcnc/apps/geberit_cutter_app/geberit_cutter_app_output.svg" % (os.getcwd(), os.getcwd())
                cmd +=  " --off M5 --on M3S%sG1Z%sF%s --feedrate %s -o %s/asmcnc/apps/geberit_cutter_app/geberit_cutter_raw_gcode.nc" % (self.speed_input.text, "-" + self.depth_input.text, self.feed_input.text, self.feed_input.text, os.getcwd())
                working_directory = os.getcwd() + '/../../svg2gcode'

            # This is required because command needs to be executed from svg2gcode folder
            subprocess.Popen(cmd.split(), cwd=working_directory).wait()

            process_gcode()

        def process_gcode():
            # Anything that svg2gcode can't be forced to do, has to be done manually

            with open(self.raw_gcode_filepath) as f:
                raw_gcode = f.readlines()

            def map_gcodes(line):
                # Stop turning off spindle throughout file by deleting all M5 commands
                if 'M5' in line:
                    line = line.replace('M5', '')
                return line
        
            processed_gcode = map(map_gcodes, raw_gcode)
            
            #Lift Z axis after each shape            
            for i in range(len(processed_gcode)):
                if 'svg > path' in processed_gcode[i]:
                    processed_gcode.insert(i+2, 'G0 Z' + str(self.z_lift_height) + '\n')

            # Lift the Z axis at end of job
            processed_gcode.insert(-1, 'G90 G0 Z' + str(self.z_lift_height) + '\n')
            # Then turn spindle off at the end            
            processed_gcode.append('M5')

            with open('./jobCache/' + self.filename_input.text, 'w+') as f:
                f.write(''.join(processed_gcode))

            self.wait_popup.popup.dismiss()
            popup_info.PopupInfo(self.sm, self.l, 500, self.l.get_str("Gcode file saved to filechooser!"))

            self.reset_editor()

        generate_svg()

    def reset_editor(self):
        self.editor_container.clear_widgets()
        self.shapes_added = 0
        self.current_shape_selection = None
        self.filename_input.text = "rectange.gcode"
        self.feed_input.text = ""
        self.speed_input.text = ""
        self.depth_input.text = ""

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
