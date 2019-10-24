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

from asmcnc.skavaUI import widget_virtual_bed, widget_status_bar,\
    widget_z_move, widget_xy_move, widget_common_move,\
    widget_quick_commands, widget_virtual_bed_control, widget_gcode_monitor,\
    widget_network_setup, widget_settings_options, widget_gcode_view
from asmcnc.geometry import job_envelope
from time import sleep


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<HomeScreen>:

    home_image_preview:home_image_preview
    file_data_label:file_data_label
    virtual_bed_container:virtual_bed_container
    status_container:status_container
    z_move_container:z_move_container
    xy_move_container:xy_move_container
    common_move_container:common_move_container
    quick_commands_container:quick_commands_container
    virtual_bed_control_container:virtual_bed_control_container
    gcode_monitor_container:gcode_monitor_container
    network_container:network_container
    settings_container:settings_container
    part_info_label:part_info_label
    home_tab:home_tab
    tab_panel:tab_panel
    pos_tab:pos_tab
    gcode_preview_container:gcode_preview_container

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
                        BoxLayout:
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            Accordion:
                                orientation: 'horizontal'

                                AccordionItem:
                                    title: 'GCode monitor'
                                    collapse: False
                                    id: gcode_monitor_container

                                AccordionItem:
                                    title: 'Network'
                                    id: network_container

                                AccordionItem:
                                    title: 'Settings'
                                    id: settings_container



                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_move_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_move_up.png'
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
                                    on_release:
                                        #root.manager.transition.direction = 'down'
                                        # Cause re-load of job file
                                        # root.m.job_gcode = [] # empties g-code object
                                        root.manager.current = 'local_filechooser'
                                        self.background_color = hex('#F4433600')
                                    on_press:
                                        self.background_color = hex('#F44336FF')
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
#                                 Button:
#                                     size_hint_x: 1
#                                     background_color: hex('#F4433600')
#                                     on_release:
#                                         root.manager.current = 'template'
#                                         self.background_color = hex('#F4433600')
#                                     on_press:
#                                         self.background_color = hex('#F44336FF')
#                                     BoxLayout:
#                                         padding: 0
#                                         size: self.parent.size
#                                         pos: self.parent.pos
#                                         Image:
#                                             source: "./asmcnc/skavaUI/img/template.png"
#                                             center_x: self.parent.center_x
#                                             y: self.parent.y
#                                             size: self.parent.width, self.parent.height
#                                             allow_stretch: True

                                Label:
                                    id: file_data_label
                                    size_hint_x: 4
                                    text_size: self.size
                                    color: 0,0,0,1
                                    markup: True
                                    text: 'Load a file...'
                                    halign: 'center'
                                    valign: 'middle'
                                    # text: 'Data'


                            BoxLayout:
                                size_hint_y: 3
                                spacing: 20
                                orientation: 'horizontal'

                                BoxLayout:
                                    padding: 10
                                    size_hint_x: 1
                                    spacing: 10
                                    orientation: 'vertical'
                                    canvas:
                                        Color:
                                            rgba: 1,1,1,1
                                        RoundedRectangle:
                                            size: self.size
                                            pos: self.pos
                                    Image:
                                        source: root.no_image_preview_path
                                        id: home_image_preview
                                    Label:
                                        text: "Test"
                                        id: part_info_label
                                        h_align: 'left'

                                BoxLayout:
                                    size_hint_x: 3
                                    padding: 10
                                    orientation: 'vertical'
                                    canvas:
                                        Color:
                                            rgba: 1,1,1,1
                                        RoundedRectangle:
                                            size: self.size
                                            pos: self.pos
                                    id: gcode_preview_container

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
#     job_q_dir = 'jobQ/'            # where file is copied if to be used next in job
    job_filename = ''
    gcode_has_been_checked_and_its_ok = False
    
    job_box = job_envelope.BoundingBox()

    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.tab_panel.switch_to(self.home_tab))

        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.job_gcode = kwargs['job']

        # Job tab
        self.gcode_preview_widget = widget_gcode_view.GCodeView()
        self.gcode_preview_container.add_widget(self.gcode_preview_widget)

        # Position tab
        self.virtual_bed_container.add_widget(widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm))

        # Status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # Bed tab
        self.virtual_bed_control_container.add_widget(widget_virtual_bed_control.VirtualBedControl(machine=self.m, screen_manager=self.sm), index=100)

        # Move tab
        self.xy_move_widget = widget_xy_move.XYMove(machine=self.m, screen_manager=self.sm)
        self.common_move_widget = widget_common_move.CommonMove(machine=self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.common_move_container.add_widget(self.common_move_widget)
        self.z_move_container.add_widget(widget_z_move.ZMove(machine=self.m, screen_manager=self.sm))

        # Settings tab
        self.gcode_monitor_widget = widget_gcode_monitor.GCodeMonitor(machine=self.m, screen_manager=self.sm)
        self.gcode_monitor_container.add_widget(self.gcode_monitor_widget)
        self.network_container.add_widget(widget_network_setup.NetworkSetup(machine=self.m, screen_manager=self.sm))
        self.settings_widget = widget_settings_options.SettingsOptions(machine=self.m, screen_manager=self.sm)
        self.settings_container.add_widget(self.settings_widget)
        
        # Quick commands
        self.quick_commands_container.add_widget(widget_quick_commands.QuickCommands(machine=self.m, screen_manager=self.sm))


    def on_enter(self): 
        log('Job loaded:')

        # File label at the top
        if self.job_gcode != []:
            self.file_data_label.text = '[b]' + self.job_filename + '[/b]'
            # Preview file
            try: 
                Clock.schedule_once(self.preview_job_file, 0.05)
            except:
                log('Unable to preview file')
            
        else:
            self.file_data_label.text = '[b]Load a file...[/b]'
            self.job_filename = ''
  
            self.job_box.range_x[0] = 0
            self.job_box.range_x[1] = 0
            self.job_box.range_y[0] = 0
            self.job_box.range_y[1] = 0
            self.job_box.range_z[0] = 0
            self.job_box.range_z[1] = 0      
            try:            
                self.gcode_preview_widget.draw_file_in_xy_plane([])
                self.gcode_preview_widget.get_non_modal_gcode([])
            except:
                print 'No G-code loaded.'
 
    def preview_job_file(self, dt):
        
        # Might leave this here for now - might change if you move datums etc.?      
        log('> get_non_modal_gcode')
        gcode_list = self.gcode_preview_widget.get_non_modal_gcode(self.job_gcode, True)

        log('< get_non_modal_gcode ' + str(len(gcode_list)))

        ###

        # Draw gcode preview
        try:
            log ('> draw_file_in_xy_plane')
            self.gcode_preview_widget.draw_file_in_xy_plane(gcode_list)
            log ('< draw_file_in_xy_plane')
        except:
            print 'Unable to draw gcode'

        # TODO tidy this up, possibly make a job class to hold extents extents and the job data
        self.job_box.range_x[0] = self.gcode_preview_widget.min_x
        self.job_box.range_x[1] = self.gcode_preview_widget.max_x
        self.job_box.range_y[0] = self.gcode_preview_widget.min_y
        self.job_box.range_y[1] = self.gcode_preview_widget.max_y
        self.job_box.range_z[0] = self.gcode_preview_widget.min_z
        self.job_box.range_z[1] = self.gcode_preview_widget.max_z

        self.part_info_label.text = ("X: " + str(self.job_box.range_x[1]-self.job_box.range_x[0]) +
                                     "\nY: " + str(self.job_box.range_y[1]-self.job_box.range_y[0]) +
                                     "\nZ: " + str(self.job_box.range_z[0]))

        # Search for tool listings and show
        for line in self.job_gcode:
            if line.find('(T') >= 0:
                self.file_data_label.text += '\n' + line.strip()
                break

        log('DONE')
        # break


# ------------------------------------------------------------------------------------
# USED IN THREADING SECTION: 

#     def load_gcode_list(self, filename, gcode_mgr_list):
#         log ('> get_non_modal_gcode thread')
#         #time.sleep(2)
#         #for x in range(10000000):
#         #    x = x + 1
#             #if x % 10000 == 0:
#             #    sleep(0.0001)
#         #log ('counted')
# 
#         gcode_list = self.gcode_preview_widget.get_non_modal_gcode(self.job_q_dir + filename)
# 
#         for line in gcode_list:
#             gcode_mgr_list.append(line)
# 
#         log ('< get_non_modal_gcode thread ' + str(len(gcode_list)))
#         return gcode_list
