import csv
import math
import json
import re
import matplotlib.pyplot as plt
import numpy as np
import time

tik = time.time()

    ############### THE DATA STRUCTURE & Algorithm #################
    # sort_doc_byLength_unzip = [(docs ), (docs lenth), [clusters of [{index:mode}],... [{index:mode}] ]
    # Each mode of each point moves by the Gaussian weight toward central of each cluster.
    # This movement is ruled by Gaussian formula and weighing by offset of distance calculation.
    # This formula "diff = abs(temp - points)/offset" put weigh to all distance calculation.
    # The higer the offset the more distance is magnified, hence the heavier the pull for each mode point.
    # Increasing this offset from 1 until ~50 will get 3 centroids (short medium long)
    ######################################################################

def distance (mode, points):
    # mode: 1 point
    # points: all points
    offset = 50 # Increasing from 1 until (here = 50) there are 3 centroids left (short medium long)
    temp = np.full(points.shape, mode)
    diff = abs(temp - points)/offset
    return diff

def distance_RGB (mode, points):
    # print('points ', points)
    # print('mode ', mode)
    # array_all = mode - points
    # print("array_all ", array_all)
    diff = np.sqrt(np.sum((mode - points)**2, axis = 1))
    return diff

def gauss(dist, bandwidth):
    # f_1 = 1.0/(bandwidth * math.sqrt(2*math.pi))
    f_2 = np.exp(-((dist**2/2))) # 2 is changable
    return f_2 

def flat_kernel(dist, bandwidth):
    if dist < bandwidth:
        return 1
    else:
        return 0

def next_postion (data_space, current_mode, band):
    # band if flat kernel
    diff = distance_RGB(current_mode, data_space)
    print('diff ', diff)
    # weight = gauss(diff, band)
    cal_band = distance_RGB(np.array([120,120,120]), np.array([140,140,140]))
    print("diff thres, ", cal_band)
    weight = flat_kernel(diff, cal_band)
    print('weight ', weight)
    if weight !=0:
        return (weight*data_space).sum(axis = 0) / weight #.sum()
    else:
        return data_space*0

# with open('file1.json', mode='r') as f:
import cv2

im = cv2.imread('test1.jpeg')
img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)   # BGR -> RGB

img = cv2.resize(img, (int(img.shape[0]/8), int(img.shape[1]/8)), interpolation = cv2.INTER_AREA)

img_size = img.shape    #hei wid channel
print(img_size)
# print(img[:10])

flat_img = np.array(img.copy()).reshape(img_size[0]*img_size[1], 3)
# print(flat_img.shape)
# print(flat_img[:10])

# rewrite_img = flat_img.reshape(img_size[0], img_size[1], 3)
# cv2.imwrite('out1.jpeg', cv2.cvtColor(rewrite_img, cv2.COLOR_BGR2RGB) )



# [1] # READ the input json file
# data = json.load(f)
# print(data[:2])

# included_cols = [17]
# rows = []
# raw_lines = []

# [1.1] # CLEAN the input lines
# for row in data:
    
#     raw_lines.append(row)
#     row = re.sub(r'[^\w\s]', '', row.lower()).split()

#     rows.append(row)    #each row is a document
    

# print('Processed {} lines.'.format(len(rows)))

# [2] # LINE length calculation
# doc_length_ls = list()

# for i, row in enumerate(rows):
    
#     doc_length_ls.append(float(len(row)))


# [3] # LINE-length ZIP
# zipped = zip(rows,doc_length_ls)
# zipped_raw =zip(raw_lines, doc_length_ls)

# sort_doc_byLength = sorted(zipped, key=lambda x: x[1]).copy()
# sort_doc_byLength_raw = sorted(zipped_raw, key=lambda x: x[1]).copy()


# sort_doc_byLength_unzip = list(zip(*sort_doc_byLength))   
# sort_doc_byLength_unzip_raw = list(zip(*sort_doc_byLength_raw))   


sort_doc_byLength_unzip = [list(flat_img)]
# [3.1] # DATA STRUCTURE for merge looping

temp = []
for idx, i in enumerate(list(flat_img)):

    temp.append([{idx:i}])    
    #nested. Each item is a mode of 1 data point. {index:mode} the index refer to the position of original data point

sort_doc_byLength_unzip.append(temp) # add list of cluster index, nested list and dict

# sort_doc_byLength_unzip = [(RGB pixels), [clusters of [{index:mode}],... [{index:mode}] ]

# [4] # CONVERGENCE
band_width = 5
data_space = np.array(sort_doc_byLength_unzip[0])

for idx, i in enumerate(sort_doc_byLength_unzip[1]):
    temp_ = tuple(sort_doc_byLength_unzip[1][idx][-1].copy().keys())[0] #get the key of the last
    converge = True
    
    prev_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
    current_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
    # point = idx     # img_size[0]*img_size[1]
    # neighbor_space = neighbors(data_space, point, neighbor_distance)
    while converge:
        #update next position of mode to current mode
        sort_doc_byLength_unzip[1][idx][-1][temp_] = next_postion(data_space, current_mode, band_width)

        
        current_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]
         
        print('current_mode ', current_mode)
        print('prev_mode ', prev_mode)
        print('minus ', abs(current_mode-prev_mode))
        if (abs(current_mode-prev_mode) <= distance_RGB(np.array([120,120,120]), np.array([125,125,125])) ).all() or current_mode.all() == 0:
        # if abs(current_mode-prev_mode) <= 1000 or current_mode == -1:
            # print('minus ', abs(current_mode-prev_mode))
            print((abs(current_mode-prev_mode) <= distance_RGB(np.array([120,120,120]), np.array([125,125,125]))).all())
            print(current_mode.all() == 0)
            print("=====  idx ", idx)
            print("len all, ", len(sort_doc_byLength_unzip[1]))
            converge = False
        prev_mode = sort_doc_byLength_unzip[1][idx][-1][temp_]#.copy()
        # break

        

centroids = []
for i in sort_doc_byLength_unzip[1]:
    centroids.append(list(i[0].values())[0])
# print("centroids raw ", np.array(centroids).astype(int))
centroids = np.unique(np.array(centroids).astype(int))
print("centroids ", centroids)

centroids_color = []
for i in centroids:
    centroids_color.append( np.array(np.random.choice(range(256), size=3)) )
# sort_doc_byLength_unzip = [(RGB pixels), [clusters of [{index:mode}],... [{index:mode}] ]

centroids_idx = {}
for i_c in centroids:
    centroids_idx[i_c] = []
    for i_s in sort_doc_byLength_unzip[1]:

        key = int(list(i_s[0].keys())[0])
        

        if np.array(list(i_s[0].values())[0]).astype(int).all() == i_c:
            
            centroids_idx[i_c].append(key)
        if key != i_c:   
            continue


# sort_doc_byLength_unzip_raw[0] [min(centroids_idx[list(centroids)[0]]): max(centroids_idx[list(centroids)[0]])+1]
mask_imge = sort_doc_byLength_unzip[0].copy()

for idx, i in enumerate(mask_imge):
    for idx_c, i_c in enumerate(centroids):
        # print("centroids_idx[i_c] ", centroids_idx[i_c])
        if idx in centroids_idx[i_c]:
            # print("masked ")
            mask_imge[idx] = centroids_color[idx_c]


rewrite_img = np.array(mask_imge).reshape(img_size[0], img_size[1], 3)
cv2.imwrite('out1.jpeg', cv2.cvtColor(rewrite_img, cv2.COLOR_BGR2RGB) )