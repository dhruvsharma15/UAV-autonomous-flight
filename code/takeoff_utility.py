# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import cv2
import numpy as np

def get_edges(matrix):                              
    matrix = np.uint8(matrix)
    edges = cv2.Canny(matrix, 10, 30)
    m, n = edges.shape
    result = edges[10:m-10, 10:n-10]
    return result