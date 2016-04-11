import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import glob
import os
from operator import itemgetter
from audioop import reverse

sys.path.append('/usr/local/lib/python2.7/dist-packages/')

def imageDistance(imgName1, imgName2, link=3):# returns distance between 2 images
    img1 = cv2.imread(imgName1)
    img2 = cv2.imread(imgName2)
    if img1 is None or img2 is None:
        print "Images not found", type(img1), imgName1, type(img2), imgName2
        exit(0)
    gray1= cv2.cvtColor(img1,cv2.COLOR_BGRA2GRAY)
    gray2= cv2.cvtColor(img2,cv2.COLOR_BGRA2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1,None)
    kp2, des2 = sift.detectAndCompute(gray2,None)
    
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    if(len(des1) >= len(des2)):
        matches = bf.match(des1,des2)
    else:
        matches = bf.match(des2,des1)
    #matches = sorted(matches, key = lambda x:x.distance)

    #img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=2)

    #plt.imshow(img3),plt.show()

    if link==1:
        return min(matches, key=lambda x: x.distance).distance
    elif link==2:
        return max(matches, key=lambda x: x.distance).distance
    else:#mean
        distSum=0
        for x in matches:
            distSum+= x.distance
        return distSum/len(matches)



def files(path):
    points=[]
    imList = glob.glob(path)
    c1=imList[0]
    for imName in imList:
        point={}
        point['name']=imName
        point['c']= c1
        #point['c']= imName
        points.append(point)
    return points, c1


if __name__ == "__main__":
    dataSet,cDS = files("../../../dataSets/*")
    queryPts,cQ = files("./queryImages/*")
    k = 3
    
    
    for p1 in queryPts:
        distancesList = []
        for p2 in dataSet:
            tempDict = {}
            tempDict['point'] = p2
            tempDict['d'] = imageDistance(p1['name'], p2['name'])
            distancesList.append(tempDict)
            
    
        distancesList = sorted(distancesList, key = lambda user: (user['d']),reverse = False)
        
        for i in range(k):
            center = p1['name']
            queryFileName = os.path.basename(center)
            dstFile = './'+queryFileName.split('.')[0]
            dstFilePath = dstFile + '/'
            if not os.path.exists(dstFile):
                os.mkdir(dstFile)
    

            srcFile = distancesList[i]['point']['name']
            #print srcFile
            os.system('cp \"'+ srcFile + '\" ' + dstFilePath)
    
    
    
    