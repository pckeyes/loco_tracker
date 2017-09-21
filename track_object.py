# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 10:49:31 2017

@author: pckeyes
"""

#import libraries
import cv2
import sys
import numpy as np

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
    roi1 = cv2.selectROI(frame, False)
    roi2 = cv2.selectROI(frame, False)
    
    
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
        
        #TODO get this shit working, will likely fix your tracking problems 
        #perform gamma correction
        curr_gamma = np.float32(curr_frame)/255
        curr_frame = np.uint8(cv2.pow(curr_gamma, .75) * 255)     
        
        #get first centroid
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        centroid = (int(((p2[0]-p1[0])/2) + p1[0]), int(((p2[1]-p1[1])/2) + p1[1]))

    
        #update tracker
        ret, bbox = tracker.update(curr_frame)
        
        #re-position bounding box
        if ret:
            #display ROIs in behavior trace window
            roi1_p1 = (int(roi1[0]), int(roi1[1]))
            roi1_p2 = (int(roi1[0] + roi1[2]), int(roi1[1] + roi1[3]))
            cv2.rectangle(trace, roi1_p1, roi1_p2, (255,0,0))
            roi2_p1 = (int(roi2[0]), int(roi2[1]))
            roi2_p2 = (int(roi2[0] + roi2[2]), int(roi2[1] + roi2[3]))
            cv2.rectangle(trace, roi2_p1, roi2_p2, (0,255,0))
            
            #display real-time tracking in tracking window
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #draw bounding box
            cv2.rectangle(curr_frame, p1, p2, (0,0,255))
            #draw center of bounding box
            curr_centroid = (int(((p2[0]-p1[0])/2) + p1[0]), int(((p2[1]-p1[1])/2) + p1[1]))
            cv2.circle(curr_frame, curr_centroid, 4, (255,0,0))
            
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