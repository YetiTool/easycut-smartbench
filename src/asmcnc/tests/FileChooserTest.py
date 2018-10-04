import kivy, os
from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp


Builder.load_string("""

<FileChooserTestScreen>:

    filechooser:filechooser


    BoxLayout:
                
        BoxLayout:
            size_hint_x: 1
            orientation: 'vertical'
            Button:
                text: 'Print selection'
                on_release: 
                    print filechooser.selection
            Button:
                text: 'Clear selection'
                on_release: 
                    filechooser.selection = []
                    print filechooser.selection
            Button:
                text: 'Update files'
                on_release: 
                    filechooser._update_files()
                    
        FileChooserListView:
            size_hint_x: 5
            rootpath: 'C:/delete_me'
            id: filechooser
            on_selection: 
                print filechooser.selection
        
""")

class FileChooserTestScreen(Screen):
    pass
 
runTouchApp(FileChooserTestScreen())
 
