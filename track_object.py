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
    
    #get user input
    video = raw_input('Enter full path to video: ')
    n_rois = int(raw_input('Enter # ROIs: '))
    n_trackers = int(raw_input('Enter # tracked objects: '))
    use_gamma = int(raw_input('If you would like to use gamma correction enter 1, else enter 0: '))
    if use_gamma:
        gamma = float(raw_input('Enter gamma correction value: '))
    
    #initialize global vars
    trackers = []
    bboxes = []
    n_bboxes = n_trackers
    centroids = [(0,0)] * n_trackers
    rois = []
    roi_vertices = {k: () for k in range(0, n_rois)}
    roi_counts_per_tracker = {k: [] for k in range(0, n_trackers)}
    for i in range(0, n_trackers):
        for j in range(0, n_rois):
            roi_counts_per_tracker[i].append(0)
    total_count = 0
    #TODO turn this into a list of x tuples with y values where x is the # of tracked objects and y is the number of ROIs
    
    #set up tracker(s)
    #tracking algorithms include: BOOSTING, MIL, KCF, TLD, MEDIANFLOW
    for i in range(0, n_trackers):
        trackers.append(cv2.Tracker_create("BOOSTING"))
    
    #read video
    cap = cv2.VideoCapture(video)
    
    #exit if video didn't open
    if not cap.isOpened():
        print "Video did not open"
        sys.exit()
    
    #grab first frame
    ret, frame = cap.read()
    if not ret:
        print "Frame was not grabbed"
        sys.exit()
        
    #gamma correct frame
    if use_gamma:
        frame = gamma_correct(frame, gamma)

    #define bounding box(es)
    for i in range(0, n_trackers):
        bboxes.append(cv2.selectROI(frame, False))

    #define ROI(s)
    for i in range(0, n_rois):
        rois.append(cv2.selectROI(frame, False))
    
    #save ROI vertices
    for i in range(0, n_rois):
        roi = rois[i]
        roi_p1, roi_p2 = get_rect_vertices(rois[i])
        roi_vertices[i] = (roi_p1, roi_p2);
    
    
    #initialize tracker(s) with first frame and bounding box(es)
    for i in range(0, n_trackers):
        ret = trackers[i].init(frame, bboxes[i])
    
    #initialize white background for tracing behavior
    trace = np.zeros((frame.shape), dtype="uint8") + 255
    
    #move through video frame by frame
    while True:
        
        #grab new frame
        ret, curr_frame = cap.read() 
        #ret, curr_frame = cap.read() #to down-sample video by 50%
        if not ret: break #break out of loop when video is out of frames
        
        #convert frame to grayscale THIS IS BROKEN DONT KNOW WHY
        #curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        #perform gamma correction
        if use_gamma:
            frame = gamma_correct(frame, gamma)
        
        #get first centroid(s)
        for i in range(0, n_trackers):    
            bbox_p1, bbox_p2 = get_rect_vertices(bboxes[i])
            centroid_p1, centroid_p2 = get_rect_centroid(bbox_p1, bbox_p2)
            centroids[i] = (int(centroid_p1), int(centroid_p2))
            #TODO write centroid(s) to file

        #display ROIs in behavior trace window
        for i in range(0, n_rois):
           cv2.rectangle(trace, roi_vertices[i][0], roi_vertices[i][1], COLORS[i]) 

        #update tracker(s)
        for i in range(0, n_trackers):
            #re-position bounding box
            ret, bboxes[i] = trackers[i].update(curr_frame)
            #ret1, bbox1 = tracker1.update(curr_frame)
            #ret2, bbox2 = tracker2.update(curr_frame)
            if ret:
                #display real-time tracking in tracking window
                bbox_p1, bbox_p2 = get_rect_vertices(bboxes[i])
                #draw bounding box
                cv2.rectangle(curr_frame, bbox_p1, bbox_p2, (0,0,255))
                #draw center of bounding box
                curr_centroid_p1, curr_centroid_p2 = get_rect_centroid(bbox_p1, bbox_p2)
                curr_centroid = (curr_centroid_p1, curr_centroid_p2)
                cv2.circle(curr_frame, curr_centroid, 4, (255,0,0))
                roi_counts_per_tracker[i] = classify_centroid(curr_centroid, roi_vertices, roi_counts_per_tracker[i])
                #trace object's path in behavior trace window
                cv2.line(trace, centroids[i], curr_centroid, (0,0,0), 1)
                #update centroid for next frame
                centroids[i] = curr_centroid
                #TODO write centroid(s) to file 

        #update total count
        total_count += 1        

        #display results
        cv2.imshow("Tracking", curr_frame)
        cv2.imshow("Behavior trace", trace)
        if cv2.waitKey(1) & 0xFF == ord('q'): break #quit upon 'q' key

#close video window
cap.release()
cv2.destroyAllWindows()

#TODO update this to reflect multiple trackers and variable ROIs
#print percentage of time in each ROI
for i in range(0, n_trackers):
    print("Object %i:" %(i + 1))
    for j in range(0, n_rois):
        #get percentages
        roi_percent = decimal.Decimal(roi_counts_per_tracker[i][j])/decimal.Decimal(total_count)
        print("Percent in ROI %i is %.3f" %(j + 1, roi_percent))
    print("")