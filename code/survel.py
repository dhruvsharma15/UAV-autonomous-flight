# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import variables
import cv2
from cv_bridge import CvBridge
import imutils
import rospy
PI = 3.1415926535

def move(pub,speed,distance):
    rate = rospy.Rate(10) # 100hz	
    variables.vel_msg.linear.x = speed	
    variables.t0 = rospy.get_time()
    current_distance = 0

    while(current_distance < distance):
        pub.publish(variables.vel_msg)
        variables.t1 = rospy.get_time()
        current_distance = abs(speed) * (variables.t1 - variables.t0)
        rate.sleep()
    variables.vel_msg.linear.x = 0
    pub.publish(variables.vel_msg)

def rotate(pub, angular_speed, angle, linear_speed):
    rate = rospy.Rate(10) # 100hz
    angular_speed = angular_speed*2*PI/360
    relative_angle = angle*2*PI/360 
    variables.vel_msg.angular.z = angular_speed
    variables.vel_msg.linear.x = linear_speed	
    variables.t0 = rospy.get_time()
    current_angle = 0
    
    while( current_angle < relative_angle):
        pub.publish(variables.vel_msg)
        variables.t1 = rospy.get_time()
        current_angle = abs(angular_speed) * (variables.t1 - variables.t0)
        rate.sleep()	
    variables.vel_msg.angular.z = 0
    pub.publish(variables.vel_msg)
 
 
def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv_image = imutils.resize(cv_image, width=400) 
    if variables.iterations%2==0:
        variables.frames.append(cv_image)    
    variables.iterations+=1
    print(variables.iterations)
    
def publish(pub):
    move(pub, 0.2, 0.5)
    rotate(pub, 25, 90, 0.2)
    move(pub, 0.2, 0.5)
    rotate(pub, 25, -90, 0.2)
    move(pub, 0.2, 0.5)
    rotate(pub, 25, 90, 0.2)		
    move(pub, 0.2, 0.5)