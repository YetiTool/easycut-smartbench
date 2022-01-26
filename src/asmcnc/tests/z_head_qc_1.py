from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_string("""
<ZHeadQC1>:
    canvas:
        Color:
            rgba: hex('#E5E5E5FF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3
            rows: 5
            spacing: dp(2)

            Label:
                text: 'FW Version: ...'

            GridLayout:
                cols: 2

                Label:
                    text: '7. Z Motors'

                GridLayout:
                    cols: 2

                    Button:
                        text: 'Up'
                    
                    Button: 
                        text: 'Down'

            Button:
                text: 'Stop'

            Button:
                text: '2. Bake GRBL Settings'

            GridLayout:
                cols: 3

                Button: 
                    text: '8. Spindle'

                Button:
                    text: '9. Laser'

                Button:
                    text: '10. Vac'

            Label:
                text: '14. X Home'

            GridLayout:
                cols: 2

                Button: 
                    text: '3. Home'

                Button: 
                    text: '4. RESET'

            GridLayout:
                cols: 2

                Label:
                    text: '11. Dust shoe'

                GridLayout:
                    cols: 3

                    Button: 
                        text: 'R'

                    Button:
                        text: 'G'

                    Button:
                        text: 'B'

            Label:
                text: '15. X Max'

            GridLayout:
                cols: 2

                Button:
                    text: '5. Test motor chips'
                #need image of cross
                Label:
                    text: '' 

            Label:
                text: '12. Temp/power'

            Label:
                text: '16. Probe'

            GridLayout:
                cols: 2

                Label:
                    text: '6. X Motors'

                GridLayout:
                    cols: 2

                    Button:
                        text: 'Up'

                    Button: 
                        text: 'Down'

            Button:
                text: '13. Disable alarms'

            Button:
                text: '17. >>> Next screen'

""")

class ZHeadQC1(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC1, self).__init__(**kwargs)