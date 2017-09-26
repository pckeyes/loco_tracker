# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:23:35 2017

@author: pckeyes
"""
import Tkinter as tk
import cv2
import numpy as np



#global variables
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
          #TODO find a way to get many colors and different colors for ROI boxes and tracking lines
SCREEN_WIDTH = tk.Tk().winfo_screenwidth()
SCREEN_HEIGHT = tk.Tk().winfo_screenheight()
          
#helper functions
def get_rect_vertices(rect):
    p1 = (int(rect[0]), int(rect[1]))
    p2 = (int(rect[0] + rect[2]), int(rect[1] + rect[3]))
    return (p1, p2)
    
def get_rect_centroid(rect_p1, rect_p2):
    p1 =  int(((rect_p2[0]-rect_p1[0])/2) + rect_p1[0])
    p2 =  int(((rect_p2[1]-rect_p1[1])/2) + rect_p1[1])
    return (p1, p2)

def classify_centroid(centroid, vertices, roi_counts):
    for i in range (0, len(roi_counts)):
        vertex1, vertex2 = vertices[i]
        if (vertex2[0] >= centroid[0] and centroid[0] >= vertex1[0] and vertex2[1] >= centroid[1] and centroid[1] >= vertex1[1]):
            roi_counts[i]+=1
            break
    return roi_counts
    
def gamma_correct(frame, gamma):
    gamma_frame = np.float32(frame)/255
    frame = np.uint8(cv2.pow(gamma_frame, gamma) * 255)  
    return frame

