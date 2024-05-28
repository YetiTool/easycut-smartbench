import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.properties import ObjectProperty
from asmcnc.skavaUI import widget_vj_polygon

Builder.load_string(
    """

<ScreenVJPolygon>

	polygon_vj: polygon_vj

	BoxLayout:

		PolygonVJ:
			id: polygon_vj

"""
)


class ScreenVJPolygon(Screen):
    polygon_vj = ObjectProperty()

    def __init__(self, **kwargs):
        super(ScreenVJPolygon, self).__init__(**kwargs)
        self.polygon_vj.sm = kwargs["screen_manager"]
