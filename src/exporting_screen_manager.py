import json
import os
from collections import OrderedDict

from kivy.uix.screenmanager import ScreenManager

SCREEN_FOLDER = os.path.join(os.path.dirname(__file__), 'screens')

if not os.path.exists(SCREEN_FOLDER):
    os.makedirs(SCREEN_FOLDER)


class ExportingScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ExportingScreenManager, self).__init__(**kwargs)

    def dump_all_screens(self):
        print("Dumping all screens")
        for screen in self.screens:
            j_obj = OrderedDict([
                ("name", screen.name),
                ("children", [])
            ])

            self.export_children(screen.children, j_obj["children"])

            with open(os.path.join(SCREEN_FOLDER, screen.name + '.json'), 'w') as f:
                json.dump(j_obj, f, indent=4)

    # def add_widget(self, screen, **kwargs):
    #     super(ExportingScreenManager, self).add_widget(screen)
    #     screen.on_enter = lambda *args: None
    #     screen.on_pre_enter = lambda *args: None
    #     screen.on_pre_leave = lambda *args: None
    #     screen.on_leave = lambda *args: None
    #     self.current = screen.name
    #
    #     j_obj = OrderedDict([
    #         ("name", screen.name),
    #         ("children", [])
    #     ])
    #
    #     self.export_children(screen.children, j_obj["children"])
    #
    #     with open(os.path.join(SCREEN_FOLDER, screen.name + '.json'), 'w') as f:
    #         json.dump(j_obj, f, indent=4)

    def export_children(self, children, j_obj_children):
        for child in children:
            child_data = OrderedDict([
                ("type", type(child).__name__),
                ("id", child.id),
                ("pos", child.pos),
                ("size", child.size),
                ("children", [])
            ])
            self.export_children(child.children, child_data["children"])
            j_obj_children.append(child_data)
