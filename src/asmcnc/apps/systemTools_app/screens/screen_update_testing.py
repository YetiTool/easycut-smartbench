"""
Created on 18 November 2020
Update testing screen for system tools app

@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.clock import Clock
import subprocess, sys, os
import csv, threading, time, textwrap
from time import sleep
Builder.load_string(
    """

<ScrollableLabelOSOutput>:
    scroll_y:1

    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        font_size: str(0.01875 * app.width) + 'sp'
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        font_size: str(0.015*app.width) + 'sp'
        text: root.text
        max_lines: 3


<UpdateTestingScreen>

    output_view: output_view

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 0.0208333333333*app.height
            orientation: "vertical"
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    font_size: str(0.01875 * app.width) + 'sp'
                    size_hint: (None,None)
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    text: "Update Testing"
                    color: hex('#f9f9f9ff')
                    font_size: 0.0375*app.width
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.666666666667*app.height)
                padding: 0.025*app.width
                spacing: 0
                orientation: 'vertical'

                GridLayout: 
                    size: self.size
                    pos: self.parent.pos
                    cols: 4
                    rows: 4
                    size_hint_y: 0.67

                    Button:
                        text: 'Ansible reset test'
                        on_press: root._ansible_reset_test()
                                
                    Button:
                        text: 'Fsck repo'
                        on_press: root._git_fsck()
                                   
                    Button:
                        text: 'Prune repo'
                        on_press: root._prune_repo()
                        
                    Button:
                        text: 'GC repo'
                        on_press: root._gc_repo()

                    Button:
                        text: 'Fetch tags'
                        on_press: root._fetch_tags()

                    Button:
                        text: 'PL ansible run'
                        on_press: root._do_platform_ansible_run()

                    Button:
                        text: 'Checkout force'
                        on_press: root._checkout_new_version()
                                   
                    Button:
                        text: ''
                        
                    Button:
                        text: ''

                    Button:
                        text: ''

                    Button:
                        text: ''

                    Button:
                        text: ''
                                   
                    Button:
                        text: ''
                        
                    Button:
                        text: ''

                    Button:
                        text: ''
                        
                    Button:
                        text: ''

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.0*app.width)
                height: dp(0.166666666667*app.height)
                padding: 0
                spacing: 0.0125*app.width
                orientation: 'horizontal'

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.1*app.width)
                    height: dp(0.166666666667*app.height)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.166666666667*app.height)
                        width: dp(0.1*app.width)
                        padding: [0.0125*app.width,0.0208333333333*app.height,0.0125*app.width,0.0208333333333*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.108333333333*app.height)
                            width: dp(0.075*app.width)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.go_back()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.775*app.width)
                    height: dp(0.166666666667*app.height)
                    padding: 0.0125*app.width
                    spacing: 0
                    orientation: 'vertical'
                    ScrollableLabelOSOutput:
                        id: output_view

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.1*app.width)
                    height: dp(0.166666666667*app.height)
                    padding: 0
                    spacing: 0

                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.166666666667*app.height)
                        width: dp(0.1*app.width)
                        padding: [0.02375*app.width,0.0208333333333*app.height,0.0125*app.width,0.0208333333333*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            size_hint: (None,None)
                            height: dp(0.125*app.height)
                            width: dp(0.06375*app.width)
                            background_color: hex('#F4433600')
                            center: self.parent.center
                            pos: self.parent.pos
                            on_press: root.exit_app()
                            BoxLayout:
                                padding: 0
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True
"""
    )
repo = 'easycut'
version = 'update_func_testing'
home_dir = '/home/pi/'
easycut_path = home_dir + 'easycut-smartbench/'


class ScrollableLabelOSOutput(ScrollView):
    text = StringProperty('')


class UpdateTestingScreen(Screen):
    WIDGET_UPDATE_DELAY = 0.2
    output_view_buffer = []

    def __init__(self, **kwargs):
        super(UpdateTestingScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['system_tools']
        self.m = kwargs['machine']
        Clock.schedule_interval(self.update_display_text, self.
            WIDGET_UPDATE_DELAY)

    def go_back(self):
        self.systemtools_sm.open_system_tools()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def add_to_user_friendly_buffer(self, message):
        self.output_view_buffer.append(str(message))
        print message

    def update_display_text(self, dt):
        self.output_view.text = '\n'.join(self.output_view_buffer)
        if len(self.output_view_buffer) > 61:
            del self.monitor_text_buffer[0:len(self.output_view_buffer) - 60]

    def run_in_shell(self, input_repo, cmd):
        if input_repo == 'easycut':
            dir_path = easycut_path
        elif input_repo == 'home':
            dir_path = home_dir
        full_cmd = cmd
        print full_cmd
        proc = subprocess.Popen(full_cmd, cwd=dir_path, stdout=subprocess.
            PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout_buffer = []
        while True:
            line = proc.stdout.readline()
            stdout_buffer.append(line)
            print line,
            if line == '' and proc.poll() != None:
                break
        stdout, stderr = proc.communicate()
        exit_code = int(proc.returncode)
        if exit_code == 0:
            bool_out = True
        else:
            bool_out = False
        self.add_to_user_friendly_buffer(bool_out)
        self.add_to_user_friendly_buffer(''.join(stdout_buffer))
        self.add_to_user_friendly_buffer(stderr)
        return [bool_out, stdout, stderr]

    def install_git_repair(self):
        install_success = self.run_in_shell(repo,
            'sudo aptitude install git-repair')

    def _repair_repo(self):
        initial_run_success = self.run_in_shell(repo, 'git-repair --force')
        if initial_run_success[0] != 0:
            install_success = self.run_in_shell(repo,
                'sudo aptitude install git-repair')
            if install_success[0] == 0:
                return self.run_in_shell(repo, 'git-repair --force')
            else:
                return install_success
        else:
            return initial_run_success

    def _git_fsck(self):
        return self.run_in_shell(repo, 'git --no-pager ' +
            'fsck --lost-found' + ' --progress')

    def _prune_repo(self):
        return self.run_in_shell(repo, 'git --no-pager ' + 'prune' +
            ' --progress')

    def _gc_repo(self):
        return self.run_in_shell(repo, 'git --no-pager ' + 'gc --aggressive')

    def _fetch_tags(self):
        return self.run_in_shell(repo, 'git --no-pager ' + 'fetch --all -t' +
            ' --progress')

    def _do_platform_ansible_run(self):
        return self.run_in_shell('home',
            '/home/pi/easycut-smartbench/ansible/templates/ansible-start.sh')

    def _checkout_new_version(self):
        return self.run_in_shell(repo, 'git --no-pager ' + 'checkout ' +
            version + ' -f' + ' --progress')

    def _ansible_reset_test(self):
        self.run_in_shell(repo, 'sudo rm ' + easycut_path + 'ansible/init.yaml'
            )
        if not self._do_platform_ansible_run()[0]:
            reset_outcome = self.run_in_shell(repo,
                'git --no-pager reset --hard')
            print 'Reset outcome'
            print reset_outcome
            if self._do_platform_ansible_run():
                print 'success!'

    def add_remotes(self):
        pass

    def remove_remotes(self):
        pass
