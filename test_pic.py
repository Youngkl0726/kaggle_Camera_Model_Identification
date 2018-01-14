import cv2
import numpy as np
file = open("TrainAug.txt")
pic_str = [[] for i in range(68184)]
for i in xrange(68184):
    line = file.readline()
    line = line.strip()
    line = line.split(" ")
    pic_str[i].append(line[0])

for i in xrange(68183, 19799, -1):
    print "/mnt/lustre/yangkunlin/kaggle_camera/data"+pic_str[i][0]
    img = cv2.imread("/mnt/lustre/yangkunlin/kaggle_camera/data"+pic_str[i][0])
    height = img.shape[0]
    if height < 299:
        print "height < 299", i