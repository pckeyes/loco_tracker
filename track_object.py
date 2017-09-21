# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 10:49:31 2017

@author: pckeyes
"""

#import libraries
import cv2
import sys
import numpy as np
import pandas as pd
from utilities import *
import decimal
          
if __name__ == '__main__':
    
    #set up tracker
    #tracking algorithms include: BOOSTING, MIL, KCF, TLD, MEDIANFLOW
    tracker = cv2.Tracker_create("BOOSTING")
    
    #read video
    cap = cv2.VideoCapture("C:\Users\pckeyes\Desktop\\test_video.avi")
    
    #exit if video didn't open
    if not cap.isOpened():
        print "Video did not open"
        sys.exit()
    
    #grab first frame
    ret, frame = cap.read()
    if not ret:
        print "Frame was not grabbed"
        sys.exit()
        
    #define ROIs
    #bbox = (0, 50, 50, 50) #define by preset dimensions
    bbox = cv2.selectROI(frame, False) # define by drawing ROI
    #eventually write this as adding ROIs to a list based on user input
    roi1 = cv2.selectROI(frame, False)
    roi2 = cv2.selectROI(frame, False)
    rois = [roi1, roi2]
    n_rois = len(rois) #fix this too
    roi_vertices = {k: () for k in range (0, n_rois)}
    roi_counts = [0] * n_rois
    for i in range(0, n_rois):
        roi = rois[i]
        roi_p1, roi_p2 = get_rect_vertices(rois[i])
        roi_vertices[i] = (roi_p1, roi_p2);

    #save ROI vertices
    
    
    #initialize tracker with first frame and bounding box
    ret = tracker.init(frame, bbox)
    
    #initialize background for tracing behavior
    trace = cv2.imread("C:\Users\pckeyes\Desktop\\trace_background.jpg")
    
    #track object through video
    while True:
        
        #grab new frame
        ret, curr_frame = cap.read() 
        #ret, frame = cap.read() #to down-sample video by 50%
        if not ret: break #break out of loop when video is out of frames
        
        #convert frame to grayscale THIS IS BROKEN DONT KNOW WHY
        #curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        #TODO make this optional and customizable 
        #perform gamma correction
        curr_gamma = np.float32(curr_frame)/255
        curr_frame = np.uint8(cv2.pow(curr_gamma, .75) * 255)     
        
        #get first centroid
        bbox_p1, bbox_p2 = get_rect_vertices(bbox)
        centroid_p1, centroid_p2 = get_rect_centroid(bbox_p1, bbox_p2)
        centroid = (int(centroid_p1), int(centroid_p2))

    
        #update tracker
        ret, bbox = tracker.update(curr_frame)
        
        #re-position bounding box
        if ret:
            #display ROIs in behavior trace window
            for i in range(0, n_rois):
                cv2.rectangle(trace, roi_vertices[i][0], roi_vertices[i][1], COLORS[i])
            
            #display real-time tracking in tracking window
            bbox_p1, bbox_p2 = get_rect_vertices(bbox)
            #draw bounding box
            cv2.rectangle(curr_frame, bbox_p1, bbox_p2, (0,0,255))
            #draw center of bounding box
            curr_centroid_p1, curr_centroid_p2 = get_rect_centroid(bbox_p1, bbox_p2)
            curr_centroid = (curr_centroid_p1, curr_centroid_p2)
            cv2.circle(curr_frame, curr_centroid, 4, (255,0,0))
            roi_counts = classify_centroid(curr_centroid, roi_vertices, roi_counts)
            
            #trace object's path in behavior trace window
            cv2.line(trace, centroid, curr_centroid, (0,0,0), 2)
            centroid = curr_centroid #update centroid for next frame 
        
        #display results
        cv2.imshow("Tracking", curr_frame)
        cv2.imshow("Behavior trace", trace)
        if cv2.waitKey(1) & 0xFF == ord('q'): break #quit upon 'q' key

#close video window
cap.release()
cv2.destroyAllWindows()

#print percentage of time in each ROI
#get total count number
total_counts = 0
for i in range(0, n_rois):
    total_counts += roi_counts[i]
#get percentages
roi_percents = [0.0] * n_rois
for i in range(0, n_rois):
    roi_percents[i] = decimal.Decimal(roi_counts[i])/decimal.Decimal(total_counts)
    print("Percent in ROI %i is %.3f" %(i + 1, roi_percents[i]))  