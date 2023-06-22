from kivy.lang import Builder
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

Builder.load_string("""

<ScreenVJPolygon>

	polygon_vj: polygon_vj

	BoxLayout:

		PolygonVJ:
			id: polygon_vj

""")

class ScreenVJPolygon(Screen):
	polygon_vj = ObjectProperty()
	def __init__(self, **kwargs):

		super(ScreenVJPolygon, self).__init__(**kwargs)
		#self.sm=kwargs['screen_manager']
		self.polygon_vj.sm = kwargs['screen_manager']
