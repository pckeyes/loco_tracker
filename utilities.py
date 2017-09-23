# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:23:35 2017

@author: pckeyes
"""
import Tkinter as tk


#global variables
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
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

def classify_centroid(centroid, vertices, counts):
    for i in range (0, len(counts)):
        vertex1, vertex2 = vertices[i]
        if (vertex2[0] >= centroid[0] and centroid[0] >= vertex1[0] and vertex2[1] >= centroid[1] and centroid[1] >= vertex1[1]):
            counts[i]+=1
            break
    return counts
    

