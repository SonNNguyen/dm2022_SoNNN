import csv
import math
import json
import re
import matplotlib.pyplot as plt
import numpy as np


    ############### THE DATA STRUCTURE & Algorithm #################
    # sort_doc_byLength_unzip = [(docs ), (docs lenth), [clusters of [{length:distance}],... [{length:distance}] ]
    # In the begin each doc is in one clusters. 1205 docs, 1205 cluster.
    # I will then merge these docs by adjacent distance to reduce number of cluster until only 3 clusters left
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

    # [3.1] # DISTANCE calulation of the adjacent lines
    adj_distance_ls = []
    for idx, i in enumerate(sort_doc_byLength):
        if idx +1 == len(sort_doc_byLength):
            continue
        adj_distance_ls.append(abs(i[1] -  sort_doc_byLength[idx+1][1])) 
    
    sort_doc_byLength_unzip = list(zip(*sort_doc_byLength))   
    sort_doc_byLength_unzip_raw = list(zip(*sort_doc_byLength_raw))   
    # print (sort_doc_byLength_unzip[1][:10])
    # print(adj_distance_ls[:10])

    # [3.2] # MIN MAX calulation of the length
    min_len = sort_doc_byLength_unzip[1][0]
    max_len = sort_doc_byLength_unzip[1][-1]
    max_distance = max_len - min_len

    # This is the distance of the longest lines to the shortest line, which equal max distance
    # Add this to adj_distance_ls so that the len(adj_distance_ls) = len(rows)
    adj_distance_ls.append(max_distance)

    # [3.3] # DATA STRUCTURE for merge looping
    # print('max_distance ', max_distance)
    distance_ls = range(max_distance)
    # print('distance_ls ', len(distance_ls))
    temp = []
    for i in sort_doc_byLength_unzip[1]:
        temp.append([{i:0}])    #nested. Each index is a cluster of 1 element. 

    sort_doc_byLength_unzip.append(temp) # add list of cluster index, nested list and dict

    ############### THE DATA STRUCTURE & Algorithm #################
    # sort_doc_byLength_unzip = [(docs ), (docs lenth), [clusters of [{length:distance}],... [{length:distance}] ]
    # In the begin each doc is in one clusters. 1205 docs, 1205 cluster.
    # I will then merge these docs by adjacent distance to reduce number of cluster until only 3 clusters left
    ######################################################################

    # print (sort_doc_byLength_unzip[2][:3])
    


    # [4] # MERGE LOOP
    for idx, i in enumerate(sort_doc_byLength_unzip[2]):    #first round. To update all adjacent distance to data structure

        temp = tuple(sort_doc_byLength_unzip[2][idx][-1].copy().keys())[0] #get the key of the last
        
        sort_doc_byLength_unzip[2][idx][-1][temp] =  adj_distance_ls[idx]
        
    # print (sort_doc_byLength_unzip[2][:10])
    # print("original lines: ", len(sort_doc_byLength_unzip[2]))
    
    
    # [4.1] # MAIN loop
    while len(sort_doc_byLength_unzip[2]) >3: # keep running until cluster out 3 groups: small, medium, large
        for e in distance_ls:   # considering a range of distance from 0 to max distance 
            merge_dist = e
            
            for idx, i in enumerate(sort_doc_byLength_unzip[2]): # all rounds

                if merge_dist == tuple(i[-1].values())[0]:  
                    # if distance to the next doc = merge distance => then, merge these 2 docs into one cluster (list)
                    
                    next_ = sort_doc_byLength_unzip[2][idx+1].copy()
                    sort_doc_byLength_unzip[2].remove(sort_doc_byLength_unzip[2][idx+1])

                    sort_doc_byLength_unzip[2][idx] = sort_doc_byLength_unzip[2][idx] + next_   #Merge

    # [5] # DONE clustering  
    print("Number of cluster: ", len(sort_doc_byLength_unzip[2]))

    print("Small Cluster \n")
    print(sort_doc_byLength_unzip[2][0][:5])
    print(sort_doc_byLength_unzip[2][0][-5:])
    print('=====\n')
    print("Medium Cluster \n")
    print(sort_doc_byLength_unzip[2][1][:5])
    print(sort_doc_byLength_unzip[2][1][-5:])
    print('=====\n')
    print("Long Cluster \n")
    print(sort_doc_byLength_unzip[2][2][:5])
    print(sort_doc_byLength_unzip[2][2][-5:])
    num = len(sort_doc_byLength_unzip[2][0]) +len(sort_doc_byLength_unzip[2][1] ) +len(sort_doc_byLength_unzip[2][2] ) 
        
        
    # print('Final lines', num)

    # Give ouput lines groups
    # [5.1] # EXPORT to 3 text files of 3 groups
    small_group = sort_doc_byLength_unzip_raw[0] [0 : len(sort_doc_byLength_unzip[2][0])]
    medium_group = sort_doc_byLength_unzip_raw[0] [ len(sort_doc_byLength_unzip[2][0]) : num -  len(sort_doc_byLength_unzip[2][2])]
    long_group = sort_doc_byLength_unzip_raw[0] [ num - len(sort_doc_byLength_unzip[2][2]) : ]

    with open('small_group.txt', 'w') as f:
        for line in small_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('medium_group.txt', 'w') as f:
        for line in medium_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

    with open('long_group.txt', 'w') as f:
        for line in long_group:
            f.write("{}\n".format(line) )
            f.write("--------------------\n")

