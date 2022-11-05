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

def gauss(dist):
    # f_1 = 1.0/(bandwidth * math.sqrt(2*math.pi))
    f_2 = np.exp(-((dist**2/2))) # 2 is changable
    return f_2

def next_postion (data_space, current_mode, band):
    # band if flat kernel
    diff = distance(current_mode, data_space)
    weight = gauss(diff)
    return (weight*data_space).sum(axis = 0) / weight.sum()


with open('file1.json', mode='r') as f:

    # [1] # READ the input json file
    data = json.load(f)
    print(data[:2])
    
    included_cols = [17]
    rows = []
    raw_lines = []
    
    # [1.1] # CLEAN the input lines
    for row in data:
        
        raw_lines.append(row)
        row = re.sub(r'[^\w\s]', '', row.lower()).split()

        rows.append(row)    #each row is a document
        
    
    print('Processed {} lines.'.format(len(rows)))

    # [2] # LINE length calculation
    doc_length_ls = list()
    
    for i, row in enumerate(rows):
        
        doc_length_ls.append(float(len(row)))

    
    # [3] # LINE-length ZIP
    zipped = zip(rows,doc_length_ls)
    zipped_raw =zip(raw_lines, doc_length_ls)

    sort_doc_byLength = sorted(zipped, key=lambda x: x[1]).copy()
    sort_doc_byLength_raw = sorted(zipped_raw, key=lambda x: x[1]).copy()

    
    sort_doc_byLength_unzip = list(zip(*sort_doc_byLength))   
    sort_doc_byLength_unzip_raw = list(zip(*sort_doc_byLength_raw))   

    # [3.1] # DATA STRUCTURE for merge looping

    temp = []
    for idx, i in enumerate(sort_doc_byLength_unzip[1]):

        temp.append([{idx:i}])    
        #nested. Each item is a mode of 1 data point. {index:mode} the index refer to the position of original data point

    sort_doc_byLength_unzip.append(temp) # add list of cluster index, nested list and dict

    # sort_doc_byLength_unzip = [(docs ), (docs lenth), [clusters of [{index:mode}],... [{index:mode}] ]
    
    # [4] # CONVERGENCE
    band_width = 5

    data_space = np.array(sort_doc_byLength_unzip[1])
    
    for idx, i in enumerate(sort_doc_byLength_unzip[2]):
        temp_ = tuple(sort_doc_byLength_unzip[2][idx][-1].copy().keys())[0] #get the key of the last
        converge = True
        
        prev_mode = sort_doc_byLength_unzip[2][idx][-1][temp_]
        current_mode = sort_doc_byLength_unzip[2][idx][-1][temp_]
        while converge:
            #update next position of mode to current mode
            sort_doc_byLength_unzip[2][idx][-1][temp_] = next_postion(data_space, current_mode, band_width)
            current_mode = sort_doc_byLength_unzip[2][idx][-1][temp_]
            if abs(current_mode-prev_mode) <= 0.01:
                
                converge = False
            prev_mode = sort_doc_byLength_unzip[2][idx][-1][temp_].copy()

    centroids = []
    for i in sort_doc_byLength_unzip[2]:
        centroids.append(list(i[0].values())[0])
    centroids = np.unique(np.array(centroids).astype(int))
    print("centroids ", centroids)


    # [5] # DONE clustering  
    centroids_idx = {}
    for i_c in centroids:
        centroids_idx[i_c] = []
        for i_s in sort_doc_byLength_unzip[2]:

            key = int(list(i_s[0].keys())[0])
            

            if int(list(i_s[0].values())[0]) == i_c:
                centroids_idx[i_c].append(key)
            if key != i_c:   
                continue
    
    small_group     = sort_doc_byLength_unzip_raw[0] [min(centroids_idx[list(centroids)[0]]): max(centroids_idx[list(centroids)[0]])+1]
    medium_group    = sort_doc_byLength_unzip_raw[0] [min(centroids_idx[list(centroids)[1]]): max(centroids_idx[list(centroids)[1]])+1]
    long_group      = sort_doc_byLength_unzip_raw[0] [min(centroids_idx[list(centroids)[2]]): max(centroids_idx[list(centroids)[2]])+1]


    # [5.1] # EXPORT to 3 text files of 3 groups
    
    with open('05_small_group.txt', 'w') as f:
        for line in small_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('05_medium_group.txt', 'w') as f:
        for line in medium_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('05_long_group.txt', 'w') as f:
        for line in long_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

print("Total time = ", time.time() - tik)	
