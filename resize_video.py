# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 14:46:53 2017

@author: pckeyes
"""
import cv2
import sys
import numpy as np


cap = cv2.VideoCapture("C:\Users\pckeyes\Desktop\\oprm1_saline.mp4")

if not cap.isOpened():
    print "Video did not open"
    sys.exit()

#create video writer object
out = cv2.VideoWriter("resized_oprm1_saline.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, (640, 360), isColor = True)

while(cap.isOpened()):
    ret, frame = cap.read()    
    if not ret:
        print "Frame was not grabbed"
        break
    resized = cv2.resize(frame, (640, 360), interpolation = cv2.INTER_AREA)
    out.write(resized)

cap.release()
cv2.destroyAllWindows()
print "video written"