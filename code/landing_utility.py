# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import cv2
import numpy as np
from vector import MyVector
import variables

def divergence(good_old, good_new, del_time):
     good_old = np.asarray(good_old)
     good_new = np.asarray(good_new)
     old_dist = np.zeros(good_old.shape)
     new_dist = np.zeros(good_new.shape)
     l = len(good_old)
     for i in range(l):
         old_dist[i] = euclidean_dist(good_old[i%l], good_old[(i+1)%l])
         new_dist[i] = euclidean_dist(good_new[i%l], good_new[(i+1)%l])
     diver = (old_dist - new_dist)/old_dist
     diver = np.average(diver)
     diver = diver/del_time
     return diver 
     
def euclidean_dist(point1, point2):
    dist = np.sqrt(np.square(point1[0] - point2[0]) + np.square(point1[1] - point2[1]))
    return dist

def draw_box(event,x,y,flags,param):
     if event == cv2.EVENT_LBUTTONDOWN:
          variables.refPt = [(x, y)]
 
	# check to see if the left mouse button was released
     elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
           variables.refPt.append((x, y))
     #return refPt
           
def calculate_direction(left_vectors, right_vectors):
    sum_left = sum_right = MyVector(0,0,0,0)    
    for i in range(len(left_vectors)):
        if i == 0:
            sum_left = left_vectors[i]
        else:
            sum_left = sum_left + left_vectors[i]
    
    for i in range(len(right_vectors)):
        if i == 0:
            sum_right = right_vectors[i]
        else:
            sum_right = sum_right + right_vectors[i]       
    total_sum = sum_left + sum_right   
    sey = total_sum.end_y
    ssy = total_sum.start_y   
    sex = total_sum.end_x
    ssx = total_sum.start_x
    if abs(sey-ssy) < 10:
        y = 'Static'
    elif sey < ssy:     
        y = 'Down'
    else:   
        y = 'Up'    
    if abs(sex-ssx) < 10:
        x = 'Static'
    elif sex < ssx:     
        x = 'Left'
    else:   
        x = 'Right'  
            
    return x, y