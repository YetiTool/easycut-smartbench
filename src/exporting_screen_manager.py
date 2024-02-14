import json
import os

from kivy.uix.screenmanager import ScreenManager

SCREEN_FOLDER = os.path.join(os.path.dirname(__file__), 'screens')

if not os.path.exists(SCREEN_FOLDER):
    os.makedirs(SCREEN_FOLDER)


class ExportingScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ExportingScreenManager, self).__init__(**kwargs)

    def add_widget(self, screen):
        super(ExportingScreenManager, self).add_widget(screen)

        j_obj = {
            "name": screen.name,
            "children": [

            ]
        }

        self.export_children(screen.children, j_obj)

        with open(os.path.join(SCREEN_FOLDER, screen.name + '.json'), 'w') as f:
            json.dump(j_obj, f, indent=4)

    def export_children(self, children, j_obj):
        for child in children:
            j_obj["children"].append({
                "type": type(child).__name__,
                "id": child.id,
                "pos": child.pos,
                "size": child.size
            })

            if len(child.children) > 0:
                self.export_children(child.children, j_obj["children"][-1])

