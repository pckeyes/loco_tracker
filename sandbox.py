# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:19:11 2017

@author: pckeyes
"""

import cv2
import numpy as np

img = cv2.imread("C:\Users\pckeyes\Desktop\\example.png")
cv2.imshow('image', img)
new_img = np.float32(img)/255
cv2.imshow('test', new_img)
pow_img = cv2.pow(new_img, 1.75) 
cv2.imshow("corrected", pow_img)
mult_img = np.uint8(pow_img * 255)
cv2.imshow("blah", mult_img)
cv2.waitKey(0)