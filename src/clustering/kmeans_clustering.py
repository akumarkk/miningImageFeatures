# This program is written for Python 2.7.9
import cv2
import os
import scandir
import numpy as np

# All global variables
images = []

def print_image(image):
    count = 0
    
    print "Printing Image ..."
    for val in image:
        print val
        count += 1
    print "Total count ", count


def imageHistograms():
    global images

    for file in scandir.scandir('../../dataSets/'):
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
    global images
    centerToImageMap = {}
    k = 5 

    print "In kmeanClustering ..."
    print inputImages
    inputImages = np.array(inputImages)
    print "Numpy Array = ", inputImages
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(inputImages, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    print "K-MEANS Center   =   ", center
    print "ret              =   ", ret
    print "Label            =   ", label
    print "len(Label)            =   ", len(label)

    idx = 0
    while idx < len(label):
        if label[idx][0] in centerToImageMap:
            centerToImageMap[label[idx][0]].append(images[idx])
        else:
            centerToImageMap[label[idx][0]] = [images[idx]]

        idx += 1

    return centerToImageMap

def clusterImages(centerToImageMap):
    print centerToImageMap

    for center in centerToImageMap:
        if not os.path.exists(str(center)):
            os.makedirs(str(center))

        for fileName in centerToImageMap[center]:
            srcFile = fileName
            dstFile = str(center) + '/'
            os.system('cp '+ srcFile + ' ' + dstFile)
    


processedImg = imageHistograms()
clusterMap = kmeanClustering(processedImg)
clusterImages(clusterMap)

