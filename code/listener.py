#!/usr/bin/env python
from __future__ import division
import sys
import rospy
import cv2
import landing
import survel
import stitching_utility
from sensor_msgs.msg import Image
#import matplotlib.pyplot as plt
import variables



def listener(arg):
    print(arg)
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(20) # Publish Rate
    
    if arg == 'landing':
        variables.subs = rospy.Subscriber('/usb_cam/image_raw', Image, landing.callback) #### Subscribe to the camera input
        while variables.height > variables.threshold_height:
            while variables.run == True and variables.iterations%3==0: #### Publishing after every 3 frames
                variables.vel_msg.linear.x = variables.velocity
                variables.velocity_publisher.publish(variables.vel_msg) #### Publishing the estimated velocity in landing.py
                print 'publishing velocity'
                variables.t0 = rospy.get_time()
                if (variables.height < variables.threshold_height):
                    variables.run = False
                    variables.vel_msg.linear.x = 0
                rate.sleep()
                
        print ("You are about to crash!!")
        print 'Accuracy: %s', str(round(((variables.landing)/(variables.landing + variables.take_off + variables.hovering))*100, 3))
        variables.velocity_publisher.publish(variables.vel_msg)
        variables.subs.unregister() #### Unsubscribe from the images
    elif arg=="takeoff":
        variables.subs = rospy.Subscriber('/usb_cam/image_raw', Image, takeoff.callback)
        
    elif arg == 'survel':
        variables.subs = rospy.Subscriber('/usb_cam/image_raw', Image, survel.callback) #### Subscribe to the camera input
        survel.publish(variables.velocity_publisher) #### Publishing velocity to go on a pre-defined path
        variables.subs.unregister()
        variables.out.release()        
        stitching_utility.stitch_images()
    #rospy.spin()

if __name__ == '__main__':
    cv2.destroyAllWindows()
    variables.init() 
    listener(str(sys.argv[1]))
