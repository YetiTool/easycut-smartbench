from kivy.lang import Builder
from kivy.uix.widget import Widget

Builder.load_string("""
<HealthCheckWidget>:
    BoxLayout:
        orientation: 'horizontal'
        pos: self.parent.pos
        size: self.parent.size
        padding: [dp(10),dp(8),dp(10),dp(8)]
        
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            
            Label:
                text: "[b]YetiPilot is disabled[/b]"
                color: [0, 0, 0, 1]
                markup: True
                
            Label:
                text: "Spindle motor health check failed.\\nRe-run before job start to enable YetiPilot."
                color: [0, 0, 0, 1]
        
        Image:
            source: "./asmcnc/skavaUI/img/spindle_check_silver.png"
""")


class HealthCheckWidget(Widget):
    def __init__(self, **kwargs):
        super(HealthCheckWidget, self).__init__(**kwargs)


if __name__ == "__main__":
    from kivy.base import runTouchApp
    runTouchApp(HealthCheckWidget())