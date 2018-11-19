import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

import math
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<PolygonVJ>:

    sides_textinput_: sides_textinput

    BoxLayout:
        padding: 20
        spacing: 20
        size: root.size
        pos: root.pos
        orientation: "vertical"
        
        BoxLayout:
            size_hint_y: 1
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            padding: 15

            canvas.before:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos

            Label:
                text: 'Bit dia:'
                size_hint_x:1
                font_size:20
                color: 0,0,0,.8
            TextInput:
                id: bit_dia_textinput
                size_hint_x: 1
                font_size:24
                multiline: False

            Label:
                text: 'Depth:'
                size_hint_x: 1
                font_size:20
                color: 0,0,0,.8
            TextInput:
                id: depth_textinput
                size_hint_x: 1
                font_size:24
                multiline: False

            Label:
                #id: sides_textinput_
                text: 'Sides:'
                size_hint_x: 1
                font_size:20
                color: 0,0,0,.8
            TextInput:
                id: sides_textinput
                text: "3"
                size_hint_x: 1
                font_size:24
                multiline: False
                on_touch_up: self.select_all()
                on_text: root.on_sides_textinput()

            Label:
                text: 'A:'
                size_hint_x: 1
                font_size:20
                color: 0,0,0,.8
            TextInput:
                id: a_textinput
                size_hint_x: 1
                font_size:24
                multiline: False

            Label:
                text: 'B:'
                size_hint_x: 1
                font_size:20
                color: 0,0,0,.8
            TextInput:
                id: b_textinput
                size_hint_x: 1
                font_size:24
                multiline: False
        
        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            size: self.parent.size
            pos: self.parent.pos
            padding: 0
            spacing: 20
            
            BoxLayout:
                size_hint_x: 6
                size: self.parent.size
                pos: self.parent.pos
                padding: 20

                canvas:
                    Color: 
                        rgba: 1,1,1,1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                    Color:
                        rgba: 1,0.5,1,1
                    Line:
                        points: root.points
                        close: True
                        width: 5

            StackLayout:
                #size_hint_x: 1
                orientation: 'bt-lr'
                #spacing: 10

                canvas:
                    Color: 
                        rgba: 1,1,1,1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos

                Button:
                    id: ok
#                    text: 'OK'
                    disabled: False
                    size_hint_y: 0.25
                    #size: [50,50]
                    background_color: hex('#FFFFFF00')
                    on_release:
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/file_select_select.png"
                            #center_x: self.parent.center_x
                            #y: self.parent.y
                            #size: self.parent.width, self.parent.height
                            #allow_stretch: True

                Button:
                    id: cancel
#                    text: 'Cancel'
                    disabled: False
                    size_hint_y:0.25
                    #size: [50,50]
                    background_color: hex('#FFFFFF00')
                    on_release:
                        root.manager.current = 'lobby'
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFFFF')
                    BoxLayout:
                        padding: 20
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_cancel
                            source: "./asmcnc/skavaUI/img/template_cancel.png"
                            #center_x: self.parent.center_x
                            #y: self.parent.y
                            #size: self.parent.width, self.parent.height
                            #allow_stretch: True 

""")


class PolygonVJ(Widget):

    sides_textinput_ = ObjectProperty()
    points = ListProperty([])
    # points = ListProperty([500, 500, 300, 300, 500, 300, 500, 400, 600, 400])


    def __init__(self, **kwargs):
        super(PolygonVJ, self).__init__(**kwargs)
        # self.add_widget(Label(text='Poop'))
        print ("__init__ " + self.sides_textinput_.text)
        
        polygon_vertices = self.compute_polygon_points()
        self.plot_ploygon(polygon_vertices)
        # print ("POINTS")
        # print (self.points)


    def on_sides_textinput(self):
        print ("on_sides_textinput " + str(self.sides_textinput_.text))
        if self.sides_textinput_.text and float(self.sides_textinput_.text) > 2:
            polygon_vertices = self.compute_polygon_points()
            self.plot_ploygon(polygon_vertices)


#    def on_sides_textinput_(self, instance, value):
#        print ("on_sides_textinput_aa ", value)
#        #self.compute_polygon()


    def compute_polygon_points(self):
        print ("compute_polygon")
        polygon_vertices = []
        # https://stackoverflow.com/questions/21690008/how-to-generate-random-vertices-to-form-a-convex-polygon-in-c
        x0 = 300
        y0 = 300
        r = 80
        sides = float(self.sides_textinput_.text)
        angle_delta_r = (math.pi / 180) * 360.0 / sides
        print ("angle_delta_r ", angle_delta_r)

        angle_r = 0
        while angle_r < 2.0 * math.pi:
            x = x0 + (r * math.cos(angle_r))
            y = y0 + (r * math.sin(angle_r))
            print("{} {}".format(x, y))
            polygon_vertices.append([x, y])
            angle_r += angle_delta_r

        print(polygon_vertices)
        return polygon_vertices


    def plot_ploygon(self, polygon_vertices):
        self.points = []
        for point in polygon_vertices:
            self.points.append(point[0])
            self.points.append(point[1])


    def generate_gcode(self):
        pass











class MyApp(App):

    def build(self):
        print ("MyApp")
        return PolygonVJ()


if __name__ == '__main__':
    MyApp().run()
