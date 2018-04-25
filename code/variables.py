# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 00:40:40 2017

@author: mohit
"""

import cv2
import rospy
from geometry_msgs.msg import Twist

def init():
    return

 ######## Calculate Accuracy ######## 
landing = 0
hovering = 0
take_off = 0

 ######## Height and Velocity Estimation ######## 
height = 1.5
threshold_height = 1
velocity = 0

 ######## Keep track of time ######## 
t0 = 0
t1 = 0

 ######## Send velocity to the P3DX on these boolean ######## 
run = False
iterations = 0

 ######## To generate height vs time and velocity vs time graph ######## 
count_arr = []
height_arr = []
velocity_arr = []
p0 = [] 

 ######## To select the region of interest and related calculations ######## 
first = True
prev = []
refPt = []

 ######## Store the frames to be stitched ######## 
frames = []  

 ######## Velocity publisher  ########      
velocity_publisher = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size = 1) 

 ######## Make Video  ########    
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_1.avi',fourcc, 20.0, (640,480))    

 ######## params for ShiTomasi corner detection ######## 
feature_params = dict( maxCorners = 200,
                        qualityLevel = 0.1,
                        minDistance = 7,
                        blockSize = 7 )
                        
 
 ######## Parameters for lucas kanade optical flow ######## 
lk_params = dict( winSize = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

 ######## Put text on the frame ######## 
font = cv2.FONT_HERSHEY_SIMPLEX
x1 = 50 #position of text
y1 = 50 #position of text
y2 = 100
y3 = 150
y4 = 200
y5 = 250
y6 = 300
del_time = 0.1
threshold = 5

 ######## Publish velocity message ######## 
vel_msg = Twist()
vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0