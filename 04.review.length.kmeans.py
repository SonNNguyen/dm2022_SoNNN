import csv
import math
import json
import re
import matplotlib.pyplot as plt
import numpy as np
import random
import copy

    ############### THE DATA STRUCTURE & Algorithm #################
    # Define a boundary (middle point between 2 centroids)
    # boundary = (centroids[idx+1] - i)/2 + i 

    # Ex: 2 centroids 15 and 31 
    # any point less than the boundary = (15+31)/2 + 15
    # will be of cluster (centroid 15) & 
    # any point more than boundary will be of cluster (centroid 31)

    # mask_cur = temp.copy()<= boundary
    # mask_next = temp.copy() > boundary
    
    # Using numpy array as mask to filter points of each cluster
    # clusters.append( temp.copy() * mask_cur * mask_prev )

    # Data point
    # [1 2 3 4 5 5 6 8 9 14 25 66 77 ]
    
    # Masks
    # [1 1 1 1 0 0 0 0 0 0  0  0  0  ]
    # [0 0 0 0 1 1 1 1 0 0  0  0  0  ]
    # [0 0 0 0 0 0 0 0 1 1  1  1  1  ]

    # centroid t0 t1 t2  
    # t0+t1/2 = bound; boundaries finding
    # new centroid
    ######################################################################

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
        
        doc_length_ls.append(len(row))

    
    # [3] # LINE-length ZIP
    zipped = zip(rows,doc_length_ls)
    zipped_raw =zip(raw_lines, doc_length_ls)

    sort_doc_byLength = sorted(zipped, key=lambda x: x[1]).copy()
    sort_doc_byLength_raw = sorted(zipped_raw, key=lambda x: x[1]).copy()


    sort_doc_byLength_unzip = list(zip(*sort_doc_byLength))   
    sort_doc_byLength_unzip_raw = list(zip(*sort_doc_byLength_raw))   
    

    ############### THE DATA STRUCTURE & Algorithm #################
    # Define a boundary (middle point between 2 centroids)
    # boundary = (centroids[idx+1] - i)/2 + i 

    # Ex: 2 centroids 15 and 31 
    # any point less than the boundary = (15+31)/2 + 15
    # will be of cluster (centroid 15) & 
    # any point more than boundary will be of cluster (centroid 31)

    # mask_cur = temp.copy()<= boundary
    # mask_next = temp.copy() > boundary
    
    # Using numpy array as mask to filter points of each cluster
    # clusters.append( temp.copy() * mask_cur * mask_prev )

    # Data point
    # [1 2 3 4 5 5 6 8 9 14 25 66 77 ]
    
    # Masks
    # [1 1 1 1 0 0 0 0 0 0  0  0  0  ]
    # [0 0 0 0 1 1 1 1 0 0  0  0  0  ]
    # [0 0 0 0 0 0 0 0 1 1  1  1  1  ]

    # centroid t0 t1 t2  
    # t0+t1/2 = bound; boundaries finding
    # new centroid
    ######################################################################

    


    # [4] # INIT centroids
    number_centroids = 3
    clusters = []
    centroids = []
    first_centroids = []
    for i in range(number_centroids):
        # randomize centroids 
        centroids.append( random.randint( 10, max(sort_doc_byLength_unzip[1])-10) )
    
    centroids.sort()
    first_centroids =centroids.copy()

    while np.isnan(first_centroids).any():
        for i in range(number_centroids):
            # randomize centroids 
            centroids.append( random.randint( 10, max(sort_doc_byLength_unzip[1])-10) )
        centroids.sort()
        first_centroids =centroids.copy()
        
    print('centroids ', centroids)


    # [5] # Convergence
    iter_ = True
    temp = np.array(sort_doc_byLength_unzip[1])
    count=0
    while iter_:
        # Iteration n
        count+=1
        print("================ ITER {} ================".format(count))
        # print(temp)
        c1_left = np.array(temp.copy()<=centroids[0])
        # print(c1_left)
        c3_right = temp.copy()>=centroids[-1]
        # c3_right = temp*mask
        mask_next = c1_left
        for idx, i in enumerate(centroids):
            mask_prev = mask_next.copy()
            # if idx ==0:
            #     mask_prev = c1_left
            print ('cen i, ', i)
            if idx == len(centroids) -1:
                mask_cur = c3_right
            else:
                boundary = (centroids[idx+1] - i)/2 + i
                mask_cur = temp.copy()<= boundary
                mask_next = temp.copy() > boundary
                print("Boundary: ", boundary)


            clusters.append( temp.copy() * mask_cur * mask_prev )

            print ("clusters[{}] {}  ".format(idx+1, np.sum(clusters[idx])))
        
        # [5.1] # Update average centroids
        _iter_ =0
        for idx, i in enumerate(centroids):
            prev_centroid = centroids[idx]
            
            if not np.sum(clusters[idx])== 0:

                ave = clusters[idx][np.nonzero(clusters[idx])].mean()
                
                centroids[idx] = ave
            
            if abs(prev_centroid - centroids[idx]) <= 5:
                _iter_ +=1
        
        if _iter_ >= len (centroids):
            iter_ = False
        print('centroids ', centroids)
    print('first_centroids ', first_centroids)
    

    


    # [6] # DONE clustering  

    # Get index of all items in clusters
    cluster_indices = []
    for idx, i in enumerate(centroids):
            nonzeroind = np.array([])
            nonzeroind = np.nonzero(clusters[idx])[0]
            cluster_indices.append(nonzeroind)

    print("Number of cluster: ", len(centroids))
    cluster_raws = []
    for i in cluster_indices:
        # print (np.array(sort_doc_byLength_unzip_raw[0])[i][:10])
        cluster_raws.append(list(np.array(sort_doc_byLength_unzip_raw[0])[i]))
    # print (list(cluster_raws[0][:10]))
    
    small_group = cluster_raws[0]
    medium_group = cluster_raws[1]
    long_group = cluster_raws[2]

    with open('04_small_group.txt', 'w') as f:
        for line in small_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('04_medium_group.txt', 'w') as f:
        for line in medium_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('04_long_group.txt', 'w') as f:
        for line in long_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    