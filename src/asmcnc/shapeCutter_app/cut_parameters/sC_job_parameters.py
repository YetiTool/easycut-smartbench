'''
Created 5 March 2020
@author: Letty
Module to store parameters and user choices for the Shape Cutter app
'''

import csv
import json

class ShapeCutterJobParameters(object):
    
    file_path = './asmcnc/shapeCutter_app/parameter_cache/'
    
    def __init__(self):
 
        # shape choices       
        self.shape_dict = {
            "shape": "",
            "cut_type": "",
            "dimensions": "",
            "units": "mm"
            }
        
        # shape dimensions
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
        
        # parameters
        self.tabs = {
            "tabs?": "",
            "width": "",
            "height": "",
            "spacing": "",
            "units": "mm"
            }
        
        self.cutter_dimensions = {
            "diameter": "",
            "cutting length": "",
            "shoulder length": "",
            "units": "mm"
            }

        self.feed_rates = {
            "xy feed rate": "",
            "z feed rate": "",
            "spindle speed": "",
            "units": "mm"
            }
        
        self.strategy_parameters = {
            "stock bottom offset": "",
            "step down": "",
            "finishing passes": "",
            "units": "mm"
            }
        
        self.parameter_dict = {
            "tabs": self.tabs,
            "cutter dimensions": self.cutter_dimensions,
            "feed rates": self.feed_rates,
            "strategy parameters": self.strategy_parameters         
            }
        
    def load_parameters(self):
        
#        display_parameters = ''
        
        r = csv.reader(open(self.file_path + 'default' + '.csv', "r"), delimiter = '\t', lineterminator = '\n')
        for row in r:
#            display_parameters = display_parameters + '\t\t\t\t\t\t'.join(row) + '\n\r'
            if ('\t'.join(row)).split('\t')[0]in self.parameter_dict:
                current_group = ('\t'.join(row)).split('\t')[0]
            else:
                if ('\t'.join(row)).split('\t')[0] in self.parameter_dict[current_group]:
                    self.parameter_dict[current_group]('\t'.join(row)).split('\t')[0] = ('\t'.join(row)).split('\t')[1]        

        output = self.parameters_to_string()
        return output
    
    def save_parameters(self, filename):
        w = csv.writer(open(self.file_path + filename + '.csv', "w"), delimiter = '\t', lineterminator = '\n')
        for param_group, group_dict in self.parameter_dict.items():
            w.writerow([param_group])
            for param, value in group_dict.items():
                w.writerow(['', param, value])
    
    def parameters_to_string(self):
        
        string_parameters = ''
        
        for param_group, group_dict in self.parameter_dict.items():
            string_parameters = string_parameters + str(param_group) + '\n\r'
            
            for param, value in group_dict.items():
                string_parameters = string_parameters + '\t' + str(param) + ':\t' + str(value) + '\n\r'

        return string_parameters
     
    def generate_cut(self):
        pass
    
    
        
        
        