import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import glob
import os
from operator import itemgetter
from audioop import reverse

sys.path.append('/usr/local/lib/python2.7/dist-packages/')

def imageDistance(imgName1, imgName2, link=1):# returns distance between 2 images
    img1 = cv2.imread(imgName1)
    img2 = cv2.imread(imgName2)
    if img1 is None or img2 is None:
        print "Images not found", type(img1), imgName1, type(img2), imgName2
        exit(0)
    orb = cv2.ORB()
    gray1= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    gray2= cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1,None)
    kp2, des2 = sift.detectAndCompute(gray2,None)
    kp1, des1 = orb.detectAndCompute(gray1,None)
    kp2, des2 = orb.detectAndCompute(gray2,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck = True)
    matches = bf.match(des1,des2)
    
    sum = 0
    for m in matches:
        sum = sum + m.distance
    sum = sum / len(matches)
    return sum

    if link==1:
        return min(matches, key=lambda x: x.distance).distance
    elif link==2:
        return max(matches, key=lambda x: x.distance).distance
    else:
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
        points.append(point)
    return points, c1


def Gonzalez(k, points, c1):
    centers=set()
    centers.add(c1)
    print c1
    for point in points:
        point.update({'c':c1})
        point.update({'distance':imageDistance(point['name'],c1)})
    for i in range (1,k):
        maxDist = -1
        c=c1
        for point in points:
            distancePtC = imageDistance(point['name'],point['c'],1)
            if distancePtC>maxDist:
                maxDist = distancePtC
                c=point['name']
        centers.add(str(c))
        for point in points:
            distancePtOC = imageDistance(point['name'],point['c'],1)
            distancePtNC = imageDistance(point['name'],c)
            #print "distance to point ",point['c']," " , distancePtOC, "distance to point ",c ," ", distancePtNC
            if distancePtOC>distancePtNC:
                point['c']=c
                point['distance']=distancePtNC
    return list(centers)

def compare(c1,c2):
    for c in c1:
        if c not in c2:
            return 1
    for c in c2:
        if c not in c1:
            return 1
    return 0

def lloyds(centers, points): # centers is a list of center image. points is a list of images
    print centers
    exit(0)
    newCenters=list(centers)
    centers.pop(0) # to make them unequal the first time.
    while(compare(centers, newCenters)!=0):
        centers=list(newCenters)
        
        clusters=[]
        for i in range(len(centers)):
            clusters.append([])

        for p in points:
            nearestD = 999999999
            nearestC=-1
            for c in range(len(centers)):
                distance = imageDistance(centers[c], p['name'])
                if distance<nearestD:
                    nearestD = distance
                    nearestC = c
            p['c']=centers[nearestC]
            clusters[nearestC].append(p)

        
        newCenters=[]
        minDist=9999999999
        for c in clusters:
            for pt in c:
                xsum+=pt['x']
                ysum+=pt['y']
            xavg=xsum/len(c)
            yavg=ysum/len(c)
            newCenters.append({'x':xavg, 'y':yavg})
    
    return centers, clusters

def clusterImages(centerToImageMap):
    #print centerToImageMap

    for center in centerToImageMap:
        if not os.path.exists(str(center)):
            os.makedirs(str(center))

        for fileName in centerToImageMap[center]:
            srcFile = fileName
            dstFile = str(center) + '/'
            print srcFile
            os.system('cp \"'+ srcFile + '\" ' + dstFile)


if __name__ == "__main__":
    dataSet,cDS = files("../../../dataSets2/*")
    queryPts,cQ = files("./queryImages/*")
    k = 3
    
    
    for p1 in queryPts:
        distancesList = []
        for p2 in dataSet:
            tempDict = {}
            tempDict['point'] = p2
            tempDict['d'] = imageDistance(p1['name'], p2['name'])
            distancesList.append(tempDict)
            
    
        distancesList = sorted(distancesList, key = lambda user: (user['d']),reverse =True)
        
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
    