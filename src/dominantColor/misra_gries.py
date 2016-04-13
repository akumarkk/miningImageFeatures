import cv2
import numpy as np

def readInput(inputFile):

    s = []
    image = cv2.imread(inputFile)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    image = [ tuple(pixel) for pixel in image ]
    #print image
    return image

def charFrequency(s):
    count = {}

    for item in s:
        if item in count:
            count[item] += 1
        else:
            count[item] = 1

    #print count

def plot_colors(colors):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    print colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster

    percent = 100/(len(colors))
    for color in colors:
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), (228, 40, 39), -1)
            startX = endX
    cv2.imwrite("dominantColors.jpg", bar)
    # return the bar chart
    return bar


def misragries(s, k):
    count = {}
    label = []

    print "Total length of set = ", len(s)
    charFrequency(s)

    for item in s:
        if item in label:
            count[item] += 1
        else:
            if len(label) < k:
                label.append(item)
                count[item] = 1
            else:
                if 0 in count.values():
                    for key in count:
                        if count[key] == 0:
                            del count[key]
                            label.remove(key)

                            count[item] = 1
                            label.append(item)
                            break
                else:
                    for key in count:
                        count[key] -= 1

    #print "Count Mapping    =   ", count

    colors = []
    for key in count:
        print key, "    &      ", count[key], "\\\\"
        colors.append(key)
    return colors


print "*************** processing SET1 ******************"
s1 = readInput("red.jpg")
for k in range(1, 3):
    print "******************* k = ", k, "**********************"
    colors = misragries(s1, k)
    plot_colors(colors)


