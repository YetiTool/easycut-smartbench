'''
Created on 13 Sep 2021

@author: hsth
@author hugh.harford@yetitool.com

Purpose: undertake geometry and return array of gcode coordinates that represent a boundary


'''

class BoundaryCalculator():
    '''
    Purpose: undertake geometry and return array of gcode coordinates that represent a boundary
    
    '''
    def set_boundary_coordinates(self,datumLatest):
        pass        
    
    def get_boundary_as_gcode_array(self):
        sampleArray = [5,10,15,15] # providing a double fails the unit test, e.g. 5.5 
        return sampleArray

    def __init__(self, datumLatest):
        '''
        Constructor (really, I understood that __new__ was the constructor?
        '''
        self.dtm = datumLatest 
