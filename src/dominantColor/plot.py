import cv2
import numpy as np

def plot_colors(colors):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    print colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster

    percent = 100/(len(colors))
    for clr in colors:
        print "processing color = ", clr, type(clr)
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        #color=(clr[0], clr[1], clr[2])
        #recColor = np.array(clr, dtype=np.int32)
        #print recColor, type(recColor)
        x,y,z = clr

        print x,y,z, clr
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), (x, y, z), -1)
        startX = endX
    cv2.imwrite("redDominantColors.jpg", bar)

rose = [(39, 40, 228), (41, 43, 231), (49, 55, 232), (44, 46, 234)]
plot_colors(rose)
