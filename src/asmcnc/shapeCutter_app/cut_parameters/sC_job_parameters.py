'''
Created 5 March 2020
@author: Letty
Module to store parameters and user choices for the Shape Cutter app
'''

class ShapeCutterJobParameters(object):
    
    def __init__(self):
        
        self.shape_dict = {
            "shape": "",
            "cut_type": "",
            "dimensions": ""
            }
        
        self.circle_dimensions = {
            "D": "",
            "Z": ""
            }
        
        self.rectangle_dimensions = {
            "X": "",
            "Y": "",
            "Z": "",
            "R": ""
            }
        
        
        self.tabs = {
            "width": "",
            "height": "",
            "spacing": ""
            }
        
        self.cutter_dimensions = {
            "diameter": "",
            "cutting length": "",
            "shoulder length": ""
            }

        self.feed_rates = {
            "cutting feed rate": "",
            "lead in feed rate": "",
            "lead out feed rate": "",
            "plunge feed rate": ""
            }
        
        self.parameter_dict = {
            "tabs": self.tabs,
            "cutter dimensions": self.cutter_dimensions,
            "feed rates": self.feed_rates            
            }
        
        