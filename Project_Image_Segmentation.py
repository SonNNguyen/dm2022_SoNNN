import csv
import math
import json
import re
import matplotlib.pyplot as plt
import numpy as np
import time

tik = time.time()

    ############### THE DATA STRUCTURE & Algorithm #################
    # sort_doc_byLength_unzip = [(RGB pixels), [clusters of [{index:mode}],... [{index:mode}] ]
    # using the same method as in meanshift lab work with word length to process image
    ######################################################################

def distance (mode, points):
    # mode: 1 point
    # points: all points
    offset = 6
    temp = np.full(points.shape, mode)
    diff = abs(temp - points)/offset
    return diff

def gauss(dist):
    # f_1 = 1.0/(bandwidth * math.sqrt(2*math.pi))
    f_2 = np.exp(-((dist**2/2))) # 2 is changable
    return f_2

def next_postion (data_space, current_mode, band):
    # band if flat kernel
    diff = distance(current_mode, data_space)
    weight = gauss(diff)
    return (weight*data_space).sum(axis = 0) / weight.sum()




import cv2


# [1] # READ and process image

im = cv2.imread('test1.jpeg')
img = cv2.cvtColor(im.copy(), cv2.COLOR_BGR2GRAY) 

# [1.1] # REDUCE image size here to run app faster
img = cv2.resize(img, (int(img.shape[0]/5), int(img.shape[1]/5)), interpolation = cv2.INTER_AREA)
# cv2.imwrite("resize_input.jpeg ",cv2.resize(im, (int(img.shape[0]/3), int(img.shape[1]/3)), interpolation = cv2.INTER_AREA))

img_size = img.shape    #hei wid channel
print(img_size)
# print(img[:10])

flat_img = np.array(img).reshape(img_size[0] * img_size[1], 1)



sort_doc_byLength_unzip = [list(flat_img)]

# [2] # DATA STRUCTURE for merge looping

temp = []
for idx, i in enumerate(list(flat_img)):

    temp.append([{idx:i}])    
    #nested. Each item is a mode of 1 data point. {index:mode} the index refer to the position of original data point

sort_doc_byLength_unzip.append(temp) # add list of cluster index, nested list and dict

# sort_doc_byLength_unzip = [(RGB pixels), [clusters of [{index:mode}],... [{index:mode}] ]

# [3] # CONVERGENCE
band_width = 5
data_space = np.array(sort_doc_byLength_unzip[0])

for idx, i in enumerate(sort_doc_byLength_unzip[1]):
    temp_ = tuple(sort_doc_byLength_unzip[1][idx][-1].copy().keys())[0] #get the key of the last
    converge = True
    print("Number of pixel converge: {}/{}".format(idx,len(sort_doc_byLength_unzip[1])))
    prev_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
    current_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
    while converge:
        #update next position of mode to current mode
        sort_doc_byLength_unzip[1][idx][-1][temp_] = next_postion(data_space, current_mode, band_width)
        current_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
        if abs(current_mode-prev_mode) <= 0.01:
            
            converge = False
        prev_mode = sort_doc_byLength_unzip[1][idx][-1][temp_].copy()

centroids = []
for i in sort_doc_byLength_unzip[1]:
    centroids.append(list(i[0].values())[0])
centroids = np.unique(np.array(centroids).astype(int))
print("centroids ", centroids)


centroids_color = []
for i in centroids:
    centroids_color.append( np.array(np.random.choice(range(256), size=3)) )

# [5] # DONE clustering  
centroids_idx = {}
for i_c in centroids:
    centroids_idx[i_c] = []
    for i_s in sort_doc_byLength_unzip[1]:

        key = int(list(i_s[0].keys())[0])
        

        if int(list(i_s[0].values())[0]) == i_c:
            centroids_idx[i_c].append(key)
        if key != i_c:   
            continue


mask_imge = sort_doc_byLength_unzip[0]


for idx, i in enumerate(mask_imge):
    
    for idx_c, i_c in enumerate(centroids):
        
        if idx in centroids_idx[i_c]:
            
            mask_imge[idx] = centroids_color[idx_c].copy()


print("centroids_color ", centroids_color)

rewrite_img = np.array(mask_imge).reshape(img_size[0], img_size[1], 3)
cv2.imwrite('out1.jpeg', rewrite_img )
print("DONE please see : out1.jpeg")