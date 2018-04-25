# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:59:09 2017

@author: mohit
"""
class MyVector:
    def __init__(self, x1, y1, x2, y2):
        self.start_x = x1
        self.start_y = y1
        self.end_x = x2
        self.end_y = y2
    
    def __str__(self):
        return "({0},{1}) to ({2},{3})".format(self.start_x, self.start_y, self.end_x, self.end_y)
        
    def __add__(self, other):
        x = (self.end_x - self.start_x) + (other.end_x - other.start_x)
        y = (self.end_y - self.start_y) + (other.end_y - other.start_y)
        
        if self.start_x < other.start_x:    
            return MyVector(self.start_x, self.start_y, self.start_x+x, self.start_y+y)
        else:
            return MyVector(other.start_x, other.start_y, other.start_x+x, other.start_y+y)
    
    def length(self):
        return abs(self.start_x-self.end_x) + abs(self.start_y-self.end_y)