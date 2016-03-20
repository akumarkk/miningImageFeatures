import cv2
import numpy as np

import sys

sys.path.append('/home/sahithi/opt/opencv/release/lib/')
 
img = cv2.imread('home.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(gray,None)
 
cv2.drawKeypoints(gray,kp,img)

cv2.imwrite('sift_keypoints.jpg',img)
