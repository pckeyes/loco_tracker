# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 14:46:53 2017

@author: pckeyes
"""
import cv2
import sys
import math
import numpy as np
import pandas as pd
from utilities import *
import decimal


cap = cv2.VideoCapture("C:\Users\pckeyes\Desktop\\oprm1_morphine.mp4")

if not cap.isOpened():
    print "Video did not open"
    sys.exit()
    
#grab first frame to generate resize dimensions

#create video writer object
out = cv2.VideoWriter("resized_oprm1_morphine.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, (640, 360), isColor = True)



while(cap.isOpened()):
    ret, frame = cap.read()    
    if not ret:
        print "Frame was not grabbed"
        sys.exit()
    curr_gamma = np.float32(frame)/255
    frame = np.uint8(cv2.pow(curr_gamma, .75) * 255)
    cv2.destroyAllWindows()
    resized = cv2.resize(frame, (640, 360), interpolation = cv2.INTER_AREA)
    #cv2.imshow("resize", resized)
    cv2.waitKey(5)
    out.write(resized)

cap.release()
cv2.destroyAllWindows()
print "video written"