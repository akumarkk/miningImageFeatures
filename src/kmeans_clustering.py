# This program is written for Python 2.7.9
import cv2
import os
import scandir

def print_image(image):
    count = 0
    
    print "Printing Image ..."
    for val in image:
        print val
        count += 1
    print "Total count ", count


def imageHistograms():
    images = []
    for file in scandir.scandir('../dataSets/'):
        if file.is_file():
            images.append(file.path)

    print images


img = cv2.imread('home.jpg')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imwrite( "grey.png", img )

imageHistograms()

