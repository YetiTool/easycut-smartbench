'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout

Builder.load_string("""


<VirtualBed>

    xBar:xBar
    carriage:carriage
    g54_zone:g54_zone
    g54_marker:g54_marker
    g28Marker:g28Marker
    virtual_bed_image:virtual_bed_image
    touch_zone:touch_zone
    
    StencilBox2:
        size: self.parent.size
        pos: self.parent.pos
        
        Scatter:
            do_rotation: False
            do_translation: True
            do_scale: True        
        
            Image:
                id: virtual_bed_image
                source: './asmcnc/skavaUI/img/virtual_bed_mini.png'
                allow_stretch: True
                keep_ratio: False
                size: self.parent.size

                Image:
                    id: touch_zone
                    source: './asmcnc/skavaUI/img/virtual_bed_touch_zone.png'
                    opacity: 0
                    allow_stretch: True
                    keep_ratio: False

                Image:
                    id: xBar
                    source: './asmcnc/skavaUI/img/virtual_x_bar.png'
                    allow_stretch: True
                    keep_ratio: True
                    height: self.parent.height
                    pos: self.parent.pos
                Image:
                    id: carriage
                    source: './asmcnc/skavaUI/img/virtual_carriage.png'
                    allow_stretch: True
                    keep_ratio: True
                    pos: self.parent.pos
                Image:
                    id: g54_zone
                    source: './asmcnc/skavaUI/img/virtual_g54_zone.png'
                    allow_stretch: True
                    keep_ratio: False
                    pos: self.parent.pos   
                    opacity: 0.7     
                Image:
                    id: g28Marker
                    source: './asmcnc/skavaUI/img/park.png'
                    allow_stretch: True
                    keep_ratio: True
                    width: self.parent.width/20
                    pos: self.parent.pos    
                Image:
                    id: g54_marker
                    source: './asmcnc/skavaUI/img/jobstart.png'
                    allow_stretch: True
                    keep_ratio: True
                    width: self.parent.width/10
                    pos: self.parent.pos  
                    
""")
    

class StencilBox2(StencilView, BoxLayout):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_down(touch)
 
    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_move(touch)
 
    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox2, self).on_touch_up(touch)
    

class VirtualBed(Widget):

    # G54: workpiece co-ordinates
    # G28: set reference point

    def __init__(self, **kwargs):
    
        super(VirtualBed, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.carriage.width = self.virtual_bed_image.width/6
        self.initialise_touch_zone_size()
        Clock.schedule_interval(self.refresh_widget, self.m.s.STATUS_INTERVAL)      # Poll for status

    def initialise_touch_zone_size(self):

        if self.m.bench_is_standard():
            self.touch_zone.size = [self.touch_zone.parent.size[0]-80, self.touch_zone.parent.size[1]-60]
            self.touch_zone.pos = [self.touch_zone.parent.pos[0]+40,self.touch_zone.parent.pos[1]+30]

        if self.m.bench_is_short():
            self.touch_zone.size = [self.touch_zone.parent.size[0]-326, self.touch_zone.parent.size[1]-60]
            self.touch_zone.pos = [self.touch_zone.parent.pos[0]+163,self.touch_zone.parent.pos[1]+30]


    def refresh_widget(self, dt):
        self.setG54PosByMachineCoords(self.m.x_wco(), self.m.y_wco())
        self.setG54SizePx()
        self.setG28PosByMachineCoords(self.m.g28_x(), self.m.g28_y())
        self.setCarriagePosByMachineCoords(self.m.mpos_x(), self.m.mpos_y())

    g54box_x0 = 0.0
    g54box_y0 = 0.0
    g54box_x1 = 0.0
    g54box_y1 = 0.0
    bedWidgetJogFeedrate = 30000
 
    def on_touch_down(self, touch):
        pass
#         if self.touch_zone.collide_point(*touch.pos): 
# #             if homeScreen.zoomToggleButton.state == 'normal': self.setCarriagePosByTouch_andGo(touch)
#             self.setCarriagePosByTouch_andGo(touch)
 
    def setCarriagePosByTouch_andGo(self, touch):
        machineX = int(((touch.y - self.touch_zone.y)/self.touch_zone.height)*self.m.grbl_x_max_travel - self.m.grbl_x_max_travel) 
        machineY = int(((self.touch_zone.x + self.touch_zone.width - touch.x)/self.touch_zone.width)*self.m.grbl_y_max_travel - self.m.grbl_y_max_travel)

        print ('Y: ', str(touch.y), str(self.touch_zone.y), str(self.touch_zone.pos[1]))
        
        self.m.quit_jog() 
        self.m.jog_absolute_xy(machineX, machineY, self.bedWidgetJogFeedrate)
                      
    def setG54SizePx(self):
 
        job_box = self.sm.get_screen('home').job_box
 
        self.g54box_x0 = job_box.range_x[0]/self.m.grbl_x_max_travel*self.touch_zone.height
        self.g54box_y0 = job_box.range_y[0]/self.m.grbl_y_max_travel*self.touch_zone.width
        self.g54box_x1 = job_box.range_x[1]/self.m.grbl_x_max_travel*self.touch_zone.height
        self.g54box_y1 = job_box.range_y[1]/self.m.grbl_y_max_travel*self.touch_zone.width
         
        self.g54_zone.width = self.g54box_y1 - self.g54box_y0
        self.g54_zone.height = self.g54box_x1 - self.g54box_x0
 
    def setG28PosByMachineCoords(self, x_mc_coords, y_mc_coords):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pos_pixels_x = pixel_datum[0] + pixel_canvas[0] - (y_mc_coords+self.m.grbl_y_max_travel)/self.m.grbl_y_max_travel*pixel_canvas[0]
        pos_pixels_y = pixel_datum[1] + (x_mc_coords+self.m.grbl_x_max_travel)/self.m.grbl_x_max_travel*pixel_canvas[1]
        self.g28Marker.y = pos_pixels_y-self.g28Marker.height/2
        self.g28Marker.x = pos_pixels_x-self.g28Marker.width/2
         
    def setG54PosByMachineCoords(self, x_mc_coords, y_mc_coords):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pos_pixels_x = pixel_datum[0] + pixel_canvas[0] - (y_mc_coords+self.m.grbl_y_max_travel)/self.m.grbl_y_max_travel*pixel_canvas[0] - self.g54box_y1
        pos_pixels_y = pixel_datum[1] + (x_mc_coords+self.m.grbl_x_max_travel)/self.m.grbl_x_max_travel*pixel_canvas[1] + self.g54box_x0
        self.g54_zone.y = pos_pixels_y
        self.g54_zone.x = pos_pixels_x
        
        pos_pixels_x = pixel_datum[0] + pixel_canvas[0] - (y_mc_coords+self.m.grbl_y_max_travel)/self.m.grbl_y_max_travel*pixel_canvas[0]
        pos_pixels_y = pixel_datum[1] + (x_mc_coords+self.m.grbl_x_max_travel)/self.m.grbl_x_max_travel*pixel_canvas[1]
        self.g54_marker.y = pos_pixels_y-self.g54_marker.height/2
        self.g54_marker.x = pos_pixels_x-self.g54_marker.width/2
     
    def setCarriagePosByMachineCoords(self, grbl_x, grbl_y):
        pixel_datum = self.touch_zone.pos
        pixel_canvas = self.touch_zone.size
        pixels_x = pixel_datum[0] + pixel_canvas[0] - (grbl_y+self.m.grbl_y_max_travel)/self.m.grbl_y_max_travel*pixel_canvas[0] 
        pixels_y = pixel_datum[1] + (grbl_x+self.m.grbl_x_max_travel)/self.m.grbl_x_max_travel*pixel_canvas[1]

        self.carriage.x = pixels_x-self.carriage.width/2        
        self.carriage.y = pixels_y-self.carriage.height/2
        self.xBar.x = pixels_x-self.xBar.width/2

