import json
import os
from collections import OrderedDict

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

SCREEN_FOLDER = os.path.join(os.path.dirname(__file__), 'screens_scaled')

if not os.path.exists(SCREEN_FOLDER):
    os.makedirs(SCREEN_FOLDER)


class ExportingScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ExportingScreenManager, self).__init__(**kwargs)

        Clock.schedule_once(self.dump_all_screens, 20)

    def dump_all_screens(self, *args):
        print("Dumping all screens")
        for screen in self.screens:
            j_obj = OrderedDict([
                ("name", screen.name),
                ("children", [])
            ])

            self.export_children(screen.children, j_obj["children"])

            with open(os.path.join(SCREEN_FOLDER, screen.name + '.json'), 'w') as f:
                json.dump(j_obj, f, indent=4)

    def export_children(self, children, j_obj_children):
        for child in children:
            child_data = OrderedDict([
                ("type", type(child).__name__),
                ("id", child.id),
                ("pos", child.pos),
                ("size", child.size),
                ("padding", child.padding if hasattr(child, "padding") else None),
                ("spacing", child.spacing if hasattr(child, "spacing") else None),
                ("font_size", child.font_size if hasattr(child, "font_size") else None),
                ("children", [])
            ])
            self.export_children(child.children, child_data["children"])
            j_obj_children.append(child_data)