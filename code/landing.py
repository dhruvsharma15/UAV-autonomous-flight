# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import cv2
import numpy as np
import rospy
import variables
import landing_utility
from cv_bridge import CvBridge
from vector import MyVector


def callback(data):
    if(variables.iterations%3==0):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        old_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        old_gray = np.uint8(old_gray)
        
        if(variables.first):
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', landing_utility.draw_box)
            while(1):
                cv2.imshow('image',old_gray)
                k = cv2.waitKey(20) & 0xFF
                if k == 27:
                    break
                elif k == ord('a'):
                    print (variables.refPt)
            
            roi = old_gray[variables.refPt[0][1]:variables.refPt[1][1],variables.refPt[0][0]:variables.refPt[1][0]]
            variables.p0 = cv2.goodFeaturesToTrack(roi, mask = None, **variables.feature_params)
            for i in range(len(variables.p0)):
                variables.p0[i][0][0]+=variables.refPt[0][0]
                variables.p0[i][0][1]+=variables.refPt[0][1]        
            
            variables.run = True
            variables.vel_msg.linear.x = abs(variables.velocity)
            variables.velocity_publisher.publish(variables.vel_msg)
            variables.first = False
            variables.prev = old_gray
        else:
            p1, st, err = cv2.calcOpticalFlowPyrLK(variables.prev, old_gray, variables.p0, None, **variables.lk_params)
            good_new = p1[st==1]
            good_old = variables.p0[st==1]
            axis = int((min(good_old[:,0]) + max(good_old[:,0]))/2)
        
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                cv_image = cv2.arrowedLine(cv_image, (c,d),(a,b),(0,127,255),2  )   #blue color for arrows
                cv_image = cv2.circle(cv_image,(a,b),3,(0,0,255),1)           #red color for circles
            
            divergence = round(landing_utility.divergence(good_old, good_new, variables.del_time),5)
            vector_left = []
            vector_right = []
            
            for m in range(good_new.shape[0]):
                go = good_old[m]
                gn = good_new[m]
                if go[0]<(axis):
                    vector_left.append(MyVector(go[0], go[1], gn[0], gn[1]))
                else: 
                    vector_right.append(MyVector(go[0], go[1], gn[0], gn[1]))
            
            vector_left = np.array(vector_left)
            vector_right = np.array(vector_right)
            x, y = landing_utility.calculate_direction(vector_left, vector_right)
            
            variables.t1 = rospy.get_time()            
            distance = variables.velocity * (variables.t1 - variables.t0)
            variables.iterations+=1
            if abs(divergence) < 0.005:
                z = 'Hovering'
            if divergence < 0.01:
                z = 'Landing'
            else:
                z = 'Taking Off'
                
            variables.height = variables.height - distance
            variables.velocity = abs(divergence * variables.height)
    
            variables.height_arr.insert(int(variables.t1 - variables.t0), variables.height)
            variables.count_arr.insert(int(variables.t1 - variables.t0), int(variables.t1 - variables.t0))
            variables.velocity_arr.insert(int(variables.t1 - variables.t0), variables.velocity)
    
            cv2.putText(cv_image, "divergence = " + str(divergence) ,(variables.x1,variables.y1), 
                variables.font,1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(cv_image, "x-axis = " + x, (variables.x1,variables.y2), 
                variables.font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(cv_image, "y-axis = " + y, (variables.x1,variables.y3), 
                variables.font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(cv_image, "z-axis = " + z, (variables.x1,variables.y4), 
                variables.font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(cv_image, "height = " + str(round(variables.height,5))+'meters', (variables.x1,variables.y5), 
                variables.font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(cv_image, "velocity = " + str(round(variables.velocity,5))+'m/s', (variables.x1,variables.y6), 
                variables.font, 1,(0,0,255),2,cv2.LINE_AA)           
            cv2.imshow('frame',cv_image)
            variables.prev = old_gray.copy()
            variables.p0 = good_new.reshape(-1,1,2)
            if z == 'Landing': 
                variables.landing +=1
            elif z == 'Taking Off':
                variables.take_off +=1
            else:
                variables.hovering +=1
            
            #### print info ############
            rospy.loginfo('height is %s velocity is %s ', str(round(variables.height, 3)), str(round(variables.velocity, 3)) )     
        k = cv2.waitKey(30) & 0xff
        if (k==27):
            return
    else:
        variables.iterations+=1
