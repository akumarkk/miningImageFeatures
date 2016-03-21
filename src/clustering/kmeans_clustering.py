# This program is written for Python 2.7.9
import cv2
import os
import scandir
import numpy as np

def print_image(image):
    count = 0
    
    print "Printing Image ..."
    for val in image:
        print val
        count += 1
    print "Total count ", count


def imageHistograms():
    images = []
    for file in scandir.scandir('../../testDataSet/'):
        if file.is_file():
            images.append(file.path)

    print "Number of Images = ", len(images)
    # convert each image into Grey image
    greyImages = []
    imgArray = []
    for img_file in images:
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        imgHist = cv2.calcHist([img],[0],None,[256],[0,256])
        cv2.normalize(imgHist, imgHist, 0, 255, cv2.NORM_MINMAX, -1)
        
        #imgHist = np.int32(np.around(imgHist))

        imgHist = imgHist.transpose()

        print "Image = ", img_file, "Len = ", len(imgHist[0]), "Graylevel Histogram = ", imgHist[0]
        imgArray.append(imgHist[0])

    return imgArray

def kmeanClustering(inputImages):
    k = 4

    print "In kmeanClustering ..."
    print inputImages
    inputImages = np.array(inputImages)
    print "Numpy Array = ", inputImages
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(inputImages, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    print "K-MEANS Center   =   ", center
    print "ret              =   ", ret
    print "Lable            =   ", label
    print "len(Lable)            =   ", len(label)
    




img = cv2.imread('home.jpg')
print "Image = ", img
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
print "Grey Image   =   ", img
print "Type(img)    =   ", type(img)
cv2.imwrite( "grey.png", img )

processedImg = imageHistograms()
kmeanClustering(processedImg)

