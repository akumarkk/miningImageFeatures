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
    for file in scandir.scandir('../../dataSets/'):
        if file.is_file():
            images.append(file.path)

    # convert each image into Grey image
    greyImages = []
    imgArray = []
    for img_file in images:
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        imgHist = cv2.calcHist([img],[0],None,[256],[0,256])
        cv2.normalize(imgHist, imgHist, 0, 255, cv2.NORM_MINMAX, -1)
        
        #hist=np.int32(np.around(hist_item))

        imgHist = imgHist.transpose()

        imgArray.append(imgHist)

    return imgArray

def kmeanClustering(inputImages):
    k = 20

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(inputImages, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    




img = cv2.imread('home.jpg')
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imwrite( "grey.png", img )

imageHistograms()

