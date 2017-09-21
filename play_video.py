# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 10:40:51 2017

@author: pckeyes
"""

import numpy as np
import cv2

cap = cv2.VideoCapture("C:\Users\pckeyes\Desktop\\test_video.avi")
print(cap.grab())

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()