from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class CoordinateLabel(BoxLayout):
    """Layout for the coordinate labels with min and max limit indicators. This class is meant to be subclassed
    and not used directly."""

    orientation = "vertical"

    _prefix = StringProperty()

    def __init__(self, prefix, **kwargs):
        super(CoordinateLabel, self).__init__(**kwargs)
        self._prefix = prefix

        self._label = Label(size_hint_y=0.5, halign="left", valign="middle")
        self._label.bind(size=self._label.setter("text_size"))
        self.add_widget(self._label)

        self._limit_label = Label(font_size="12sp", size_hint_y=0.3, halign="left", valign="middle")
        self._limit_label.bind(size=self._limit_label.setter("text_size"))

    def _on_value(self, instance, value):
        self._label.text = "{0}: {1:.2f}".format(self._prefix, value)

    def _on_min_limit(self, instance, value):
        if value:
            if not self._limit_label.parent:
                self.add_widget(self._limit_label)
            self._limit_label.text = "MIN"
        else:
            self.remove_widget(self._limit_label)

    def _on_max_limit(self, instance, value):
        if value:
            if not self._limit_label.parent:
                self.add_widget(self._limit_label)
            self._limit_label.text = "MAX"
        else:
            self.remove_widget(self._limit_label)


class MachineXCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(MachineXCoordinateLabel, self).__init__("mX", **kwargs)
        self._on_value(None, serial_connection.m_x)
        serial_connection.bind(m_x=self._on_value)
        serial_connection.bind(limit_x=self._on_min_limit)
        serial_connection.bind(limit_X=self._on_max_limit)


class MachineYCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(MachineYCoordinateLabel, self).__init__("mY", **kwargs)
        self._on_value(None, serial_connection.m_y)
        serial_connection.bind(m_y=self._on_value)
        serial_connection.bind(limit_y=self._on_min_limit)
        serial_connection.bind(limit_Y=self._on_max_limit)


class MachineZCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(MachineZCoordinateLabel, self).__init__("mZ", **kwargs)
        self._on_value(None, serial_connection.m_z)
        serial_connection.bind(m_z=self._on_value)
        serial_connection.bind(limit_z=self._on_min_limit)


class WorkingXCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(WorkingXCoordinateLabel, self).__init__("wX", **kwargs)
        self._on_value(None, serial_connection.w_x)
        serial_connection.bind(w_x=self._on_value)


class WorkingYCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(WorkingYCoordinateLabel, self).__init__("wY", **kwargs)
        self._on_value(None, serial_connection.w_y)
        serial_connection.bind(w_y=self._on_value)


class WorkingZCoordinateLabel(CoordinateLabel):
    def __init__(self, serial_connection, **kwargs):
        super(WorkingZCoordinateLabel, self).__init__("wZ", **kwargs)
        self._on_value(None, serial_connection.w_z)
        serial_connection.bind(w_z=self._on_value)


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.slider import Slider


    class CoordinateLabelApp(App):
        def on_slider_value(self, instance, value):
            if value == 0:
                self.label._on_min_limit(None, True)
            elif value == 100:
                self.label._on_max_limit(None, True)
            else:
                self.label._on_min_limit(None, False)
                self.label._on_max_limit(None, False)

            self.label._on_value(None, value)

        def build(self):
            box = BoxLayout(orientation="vertical")

            self.label = CoordinateLabel("X")
            slider = Slider(min=0, max=100, value=0)
            slider.bind(value=self.on_slider_value)

            box.add_widget(self.label)
            box.add_widget(slider)
            return box


    CoordinateLabelApp().run()
