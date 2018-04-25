# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 22:30:02 2017

@author: mohit
"""
import cv2
import numpy as np
import variables
from panorama import Stitcher

def preprocess(frame):
    (h, w, c) = np.shape(frame)
    h_start = 0
    w_start = 0
    h_end = 0
    w_end = 0
    for i in xrange(h-1,-1,-1):
        if (np.sum(frame[i,:,0])!=0 and np.sum(frame[i,:,1])!=0 and np.sum(frame[i,:,2])!=0):
            h_end = i+1
            break
    for j in xrange(w-1,-1,-1):
        if (np.sum(frame[:,j,0])!=0 and np.sum(frame[:,j,1])!=0 and np.sum(frame[:,j,2])!=0):
            w_end = j+1
            break
    for i in range(h-1):
        if (np.sum(frame[i,:,0])!=0 and np.sum(frame[i,:,1])!=0 and np.sum(frame[i,:,2])!=0):
            h_start= i-1
            break
    for j in range(w-1):
        if (np.sum(frame[:,j,0])!=0 and np.sum(frame[:,j,1])!=0 and np.sum(frame[:,j,2])!=0):
            w_start = j-1
            break
    
    frame = frame[h_start:h_end,w_start:w_end,:]
    return frame


def stitch_images():
    stitcher = Stitcher()
    frames_len = len(variables.frames)
    result = variables.frames[frames_len - 1]

    for i in xrange(frames_len - 1,-1,-1):
        (result,viz) = stitcher.stitch([variables.frames[i], result], showMatches=True)
        result = preprocess(result)
        progress = (i*100/frames_len)
        if progress%5 == 0:
            print(str(progress) + " percent left")
            cv2.imwrite('/home/dhruv/stitching/web2/result'+str(i)+'.jpg',result)

def publish():
    return