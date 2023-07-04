from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line

import svgwrite
import math


class LineDrawingWidget(Widget):

    lines = []

    def on_touch_down(self, touch):
        with self.canvas:
            # ud allows storing of data in a dictionary exclusive to current touch
            touch.ud['start'] = (touch.x, touch.y)
            touch.ud['line'] = Line(points=(touch.x, touch.y))

            # Snap to other lines by checking distances (could be optimised?) (and should change to nearest neighbour rather than first match)
            for line in self.lines:
                if math.sqrt((touch.x - line[0])**2 + (touch.y - line[1])**2) < 10:
                    touch.ud['start'] = (line[0], line[1])
                    break
                elif math.sqrt((touch.x - line[2])**2 + (touch.y - line[3])**2) < 10:
                    touch.ud['start'] = (line[2], line[3])
                    break

    def on_touch_move(self, touch):
        touch.ud['line'].points = [touch.ud['start'][0], touch.ud['start'][1], touch.x, touch.y]

    def on_touch_up(self, touch):
        if touch.ud.get('start'):
            self.lines.append([touch.ud['start'][0], touch.ud['start'][1], touch.x, touch.y])


class LineDrawingApp(App):

    def build(self):
        parent = Widget()
        self.line_drawing_widget = LineDrawingWidget()

        clear_button = Button(text='Clear')
        clear_button.bind(on_release=self.clear_canvas)

        save_svg_button = Button(text='Save')
        save_svg_button.bind(on_release=self.save_svg)

        button_layout = BoxLayout()
        button_layout.add_widget(clear_button)
        button_layout.add_widget(save_svg_button)

        parent.add_widget(self.line_drawing_widget)
        parent.add_widget(button_layout)
        return parent

    def clear_canvas(self, *args):
        self.line_drawing_widget.canvas.clear()
        self.line_drawing_widget.lines = []

    def save_svg(self, *args):
        dwg = svgwrite.Drawing(filename='test.svg', size=(self.root.width,self.root.height))
        for line in self.line_drawing_widget.lines:
            # Note that when a line is drawn a scaling and translation is applied, which vertically flips the svg
            # This is needed because kivy measures Y coords from the opposite end of the screen and draws stuff upside down
            dwg.add(dwg.line((line[0], line[1]), (line[2], line[3]), stroke=svgwrite.rgb(0, 0, 0, '%'), transform="scale(1,-1) translate(0,%s)" % -self.root.height))
        dwg.save()


if __name__ == '__main__':
    LineDrawingApp().run()