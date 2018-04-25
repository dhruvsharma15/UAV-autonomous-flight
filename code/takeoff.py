
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import cv2
import numpy as np
import variables
import takeoff_utility
from cv_bridge import CvBridge
from math import pi

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    old_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    edges = takeoff_utility.get_edges(old_gray)
    lines = cv2.HoughLines(edges,1,np.pi/180,200) 
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            angle = str(round(90-(180/pi)*theta, 2))
    else:
        angle = 'Not Detected'
        
    cv2.putText(old_gray, "Angle = " + angle ,(variables.x1, variables.y1), 
                variables.font,1,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow('frame',old_gray)
    k = cv2.waitKey(30) & 0xff
    
    variables.vel_msg.linear.x = -0.2
    variables.velocity_publisher.publish(variables.vel_msg)
    variables.completed = True
    if (k==27):
        return