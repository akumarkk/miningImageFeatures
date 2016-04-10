import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import glob
import os

sys.path.append('/usr/local/lib/python2.7/dist-packages/')



def imageDistance(imgName1, imgName2, link=3):# returns distance between 2 images
	img1 = cv2.imread(imgName1)
	img2 = cv2.imread(imgName2)
	if img1 is None or img2 is None:
		print "Images not found", type(img1), imgName1, type(img2), imgName2
		exit(0)
	gray1= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
	gray2= cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	sift = cv2.xfeatures2d.SIFT_create()
	kp1, des1 = sift.detectAndCompute(gray1,None)
	kp2, des2 = sift.detectAndCompute(gray2,None)
	bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
	matches = bf.match(des1,des2)

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
		points.append(point)
	return points, c1


def Gonzalez(k, points, c1):
	print "starting gonzy"
	centers=set()
	x = raw_input('Write center name or n if you want me to choose: ')
	print x
	if x!='n':
		c1 = '../../dataSets/'+x

	centers.add(c1)
	print c1
	for point in points:
		point.update({'c':c1})
		point.update({'distance':imageDistance(point['name'],c1)})
	for i in range (1,k):
		maxDist = -1
		c=c1
		for point in points:
			distancePtC = imageDistance(point['name'],point['c'])
			if distancePtC>maxDist:
				maxDist = distancePtC
				c=point['name']
		centers.add(str(c))
		for point in points:
			distancePtOC = imageDistance(point['name'],point['c'])
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
	newCenters=list(centers)
	cent=centers.pop(2) # to make them unequal the first time.
	times = 3
	while(times>0):
		centers=list(newCenters)
		print len(centers), "---95---"
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
		
		for c in clusters:
			print len(c)

		times-=1
		print times
		continue
		newCenters=[]
		minDist=9999999999
		center=''
		distancesSaved={}
		for c in clusters:
			print len(clusters), len(c), " number of clusters, and number of points in each cluster"
			count=0
			for pt1 in c:
				sumDist=0
				for pt2 in c:
					count+=1
					print count," count"
					if pt1['name']<pt2['name']:
						x = (pt1['name'],pt2['name'])
					else:
						x = (pt2['name'],pt1['name'])

					if x in distancesSaved:
						val = distancesSaved[x]
					else:
						val = np.power(imageDistance(pt1['name'],pt2['name']),2)
						distancesSaved[x]=val

					sumDist+= val
				
				if minDist>sumDist:
					minDist=sumDist
					center=pt1['name']
			newCenters.append(center)
	print len(centers),"---146---"
	return centers, clusters

def clusterImages(centerToImageMap):
    #print centerToImageMap

    for center in centerToImageMap:
        if not os.path.exists(str(center)):
            os.makedirs(str(center))

        for fileName in centerToImageMap[center]:
            srcFile = fileName
            dstFile = str(center) + '/'
            os.system('cp \"'+ srcFile + '\" ' + dstFile)


def main():
	points,c1=files("../../dataSets/*")
	k=3
	#centers= Gonzalez(k,points,c1)
	centers = ['../../dataSets/Baseball_.jpg', '../../dataSets/chef-specialties-14200-professional-series-14-1-2-customizable-grill-mill-baseball-bat-pepper-mill.jpg', '../../dataSets/img-thing.jpg']
	points = [{'distance': 261.2919604437692, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball-large-1.jpg'}, {'distance': 271.36981928507487, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/1150SFR-2.jpg'}, {'distance': 299.62686694231155, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/1b404498-b7b8-44e8-85d3-23fff5e5395b.jpg'}, {'distance': 303.7726349623307, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/2013-02-25_00004.jpg'}, {'distance': 309.7969883282979, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/2013_Baseball_glove2012040424._V386376726_.jpg'}, {'distance': 298.0247405578043, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/310654M01 (1).jpg'}, {'distance': 292.06456663842295, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/310654M01 (2).jpg'}, {'distance': 292.06456663842295, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/310654M01.jpg'}, {'distance': 306.71920147831577, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/51YER+oAbaL._SY300_.jpg'}, {'distance': 311.9697136714541, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/8069-1_display.jpg'}, {'distance': 268.09523203793697, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/9-inch-handmade-Baseball-Ball-for-children-s-training-baseball-softball-kids-baseball-balls-game-sport.jpg'}, {'distance': 310.24679005940754, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/ash_clear_baseball_bat1_3.jpg'}, {'distance': 305.149411452444, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball-bat.jpg'}, {'distance': 275.1050336970839, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball-icon.png'}, {'distance': 256.8518034976186, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball.jpg'}, {'distance': 251.25533689815757, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball1).jpg'}, {'distance': 0.0, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/Baseball_.jpg'}, {'distance': 262.6793841044108, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball_1600_clr_11646.png'}, {'distance': 272.8768889328529, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball_3.png'}, {'distance': 238.9001382191976, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/baseball_bat_cm-f.jpg'}, {'distance': 287.9864354469407, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/cddfa81560c7da378eca2b060eec3cb3.jpg'}, {'distance': 0.0, 'c': '../../dataSets/chef-specialties-14200-professional-series-14-1-2-customizable-grill-mill-baseball-bat-pepper-mill.jpg', 'name': '../../dataSets/chef-specialties-14200-professional-series-14-1-2-customizable-grill-mill-baseball-bat-pepper-mill.jpg'}, {'distance': 281.4659144083659, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/download (1).jpg'}, {'distance': 272.2540369807063, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/download.jpg'}, {'distance': 302.982531015174, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/il_570xN.335862384.jpg'}, {'distance': 0.0, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/img-thing.jpg'}, {'distance': 292.39212783044127, 'c': '../../dataSets/img-thing.jpg', 'name': '../../dataSets/infield-baseball-glove-1.jpg'}, {'distance': 318.9177953880953, 'c': '../../dataSets/chef-specialties-14200-professional-series-14-1-2-customizable-grill-mill-baseball-bat-pepper-mill.jpg', 'name': '../../dataSets/louisville-slugger-bat.png'}, {'distance': 318.0376394567355, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/mizuno-mzm271-youth-little-league-maple-wood-baseball-bat-2.jpg'}, {'distance': 252.970651358793, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/MP910220738.jpg'}, {'distance': 270.0766422662709, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/rawlings-pro-preferred-pros1175cbr-11-75-baseball-glove-right-hand-throw-11.jpg'}, {'distance': 248.37743021870216, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/SportsAttack_leather_baseball_large.jpg'}, {'distance': 255.0884132385254, 'c': '../../dataSets/Baseball_.jpg', 'name': '../../dataSets/_32.jpg'}]
	print "gonzy done, starting lloyd"
	centers, clusters = lloyds(centers,points)
#	for x in centers:
#		print x

#	for y in points:
#		print y
#	print centers
#	print points

	clusters={i:[] for i in range(k)}

	fault=0
	for point in points:
		for i in range(k):
			print point,len(centers)
			if point['c']==centers[i]:
				clusters[i].append(point['name'])
			if point['c']!=centers[i]:
				if point['distance']>imageDistance(point['name'],centers[i]):
					fault+=1

	print clusters
	clusterImages(clusters)
	print fault

main()