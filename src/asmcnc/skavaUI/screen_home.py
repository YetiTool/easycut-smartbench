'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from __builtin__ import file
from kivy.clock import Clock

import os, sys, threading
from datetime import datetime
from multiprocessing import Process, Manager

from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar, widget_z_move, widget_xy_move, widget_common_move, widget_quick_commands # @UnresolvedImport
from asmcnc.skavaUI import widget_virtual_bed_control, widget_gcode_monitor, widget_network_setup, widget_settings_options, widget_gcode_view # @UnresolvedImport
from asmcnc.skavaUI import popup_info
from asmcnc.geometry import job_envelope # @UnresolvedImport
from time import sleep


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<HomeScreen>:

    file_data_label:file_data_label
    virtual_bed_container:virtual_bed_container
    status_container:status_container
    z_move_container:z_move_container
    xy_move_container:xy_move_container
    common_move_container:common_move_container
    quick_commands_container:quick_commands_container
    virtual_bed_control_container:virtual_bed_control_container
    gcode_monitor_container:gcode_monitor_container
    home_tab:home_tab
    tab_panel:tab_panel
    pos_tab:pos_tab
    gcode_preview_container:gcode_preview_container
    move_tab:move_tab

    BoxLayout:
        padding: 0
        spacing: 10
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.9
            padding: 0
            spacing: 10
            orientation: "horizontal"

            BoxLayout:
                size_hint_x: 0.9

                TabbedPanel:
                    id: tab_panel
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_default_tab: False
                    tab_pos: 'left_top'
                    tab_height: 90
                    tab_width: 90

                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_set_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_set_up.png'
                        on_press: root.m.laser_off()
                        BoxLayout:
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                id: gcode_monitor_container


                    TabbedPanelItem:
                        id: move_tab
                        background_normal: 'asmcnc/skavaUI/img/tab_move_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_move_up.png'
                        on_press: root.m.laser_on()
                        BoxLayout:
                            orientation: 'horizontal'
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_x: 3
                                id: xy_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                            BoxLayout:
                                size_hint_x: 1
                                id: common_move_container

                            BoxLayout:
                                size_hint_x: 2
                                id: z_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos


                    TabbedPanelItem:
                        id: pos_tab
                        background_normal: 'asmcnc/skavaUI/img/tab_pos_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_pos_up.png'
                        on_press: root.m.laser_on()
                        BoxLayout:
                            orientation: 'vertical'
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 5
                                padding: 10
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                id: virtual_bed_container

                            BoxLayout:
                                size_hint_y: 1
                                id: virtual_bed_control_container


                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_job_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_job_up.png'
                        on_press: root.m.laser_off()
                        id: home_tab
                        BoxLayout:
                            orientation: 'vertical'
                            padding: 20
                            spacing: 20
                            id: job_container
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1
                                padding: 10
                                spacing: 10
                                orientation: 'horizontal'
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                                Button:
                                    size_hint_x: 1
                                    background_color: hex('#F4433600')
                                    on_press:
                                        root.manager.current = 'local_filechooser'
                                    BoxLayout:
                                        padding: 0
                                        size: self.parent.size
                                        pos: self.parent.pos
                                        Image:
                                            source: "./asmcnc/skavaUI/img/load_file.png"
                                            center_x: self.parent.center_x
                                            y: self.parent.y
                                            size: self.parent.width, self.parent.height
                                            allow_stretch: True

                                Label:
                                    id: file_data_label
                                    size_hint_x: 4
                                    text_size: self.size
                                    font_size: '20sp'
                                    markup: True
                                    text: '[color=333333]Load a file...[/color]'
                                    halign: 'center'
                                    valign: 'middle'

                            BoxLayout:
                                size_hint_y: 3
                                padding: 20
                                orientation: 'horizontal'
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                BoxLayout:
                                    id: gcode_preview_container
                                    size_hint_x: 1
                                    orientation: 'vertical'


            BoxLayout:
                size_hint_x: 0.1
                id: quick_commands_container

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")

def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class HomeScreen(Screen):

    no_image_preview_path = 'asmcnc/skavaUI/img/image_preview_inverted.png'
    job_filename = ''
    gcode_has_been_checked_and_its_ok = False
    non_modal_gcode_list = []
    job_box = job_envelope.BoundingBox()
    default_datum_choice = 'spindle'
    z_datum_reminder_flag = False
    has_datum_been_reset = False

    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.tab_panel.switch_to(self.home_tab))

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.job_gcode = kwargs['job']
        self.set = kwargs['settings']
        self.l = kwargs['localization']

        # Job tab
        self.gcode_preview_widget = widget_gcode_view.GCodeView()
        self.gcode_preview_container.add_widget(self.gcode_preview_widget)

        # Position tab
        self.virtual_bed_container.add_widget(widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm))

        # Status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # Bed tab
        self.virtual_bed_control_container.add_widget(widget_virtual_bed_control.VirtualBedControl(machine=self.m, screen_manager=self.sm, localization=self.l), index=100)

        # Move tab
        self.xy_move_widget = widget_xy_move.XYMove(machine=self.m, screen_manager=self.sm)
        self.common_move_widget = widget_common_move.CommonMove(machine=self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.common_move_container.add_widget(self.common_move_widget)
        self.z_move_container.add_widget(widget_z_move.ZMove(machine=self.m, screen_manager=self.sm))

        # Settings tab
        self.gcode_monitor_widget = widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm)
        self.gcode_monitor_container.add_widget(self.gcode_monitor_widget)
        
        # Quick commands
        self.quick_commands_container.add_widget(widget_quick_commands.QuickCommands(machine=self.m, screen_manager=self.sm, localization=self.l))

    def on_enter(self): 

        if (self.tab_panel.current_tab == self.move_tab or self.tab_panel.current_tab == self.pos_tab):
            Clock.schedule_once(lambda dt: self.m.laser_on(), 0.2)
        else: 
            Clock.schedule_once(lambda dt: self.m.set_led_colour('GREEN'), 0.2)
        
        # File label at the top
        if self.job_gcode != []:
            
            if sys.platform == 'win32':
                self.file_data_label.text = "[color=333333]" + self.job_filename.split("\\")[-1] + "[/color]"
            else:
                self.file_data_label.text = "[color=333333]" + self.job_filename.split("/")[-1] + "[/color]"
                
            # Preview file
            try: 
                Clock.schedule_once(self.preview_job_file, 0.05)
            except:
                log('Unable to preview file')
            
        else:

            self.file_data_label.text = ('[color=333333]' + \
                self.l.get_str('Load a file') + '...' + '[/color]'
                )
            self.job_filename = ''
  
            self.job_box.range_x[0] = 0
            self.job_box.range_x[1] = 0
            self.job_box.range_y[0] = 0
            self.job_box.range_y[1] = 0
            self.job_box.range_z[0] = 0
            self.job_box.range_z[1] = 0
            
            # Hack to clear any previous job files
            try:            
                self.gcode_preview_widget.draw_file_in_xy_plane([])
                self.gcode_preview_widget.get_non_modal_gcode([])
            except:
                print 'No G-code loaded.'


    def preview_job_file(self, dt):

        # Draw gcode preview 
        try:
            log ('> draw_file_in_xy_plane')
            self.gcode_preview_widget.draw_file_in_xy_plane(self.non_modal_gcode_list)
            log ('< draw_file_in_xy_plane')
        except:
            print 'Unable to draw gcode'

        log('DONE')

    def on_pre_leave(self):
        self.m.laser_off()
    