import csv
import math
import json
import re
import matplotlib.pyplot as plt
import numpy as np


with open('file1.json', mode='r') as f:
    data = json.load(f)
    print(data[:2])
    
    included_cols = [17]
    rows = []
    raw_lines = []
    
    for row in data:
        
        raw_lines.append(row)
        row = re.sub(r'[^\w\s]', '', row.lower()).split()

        rows.append(row)    #each row is a document
        
    # print('rows: ', rows[:2])
    print('Processed {} lines.'.format(len(rows)))
    doc_length_dict = dict()
    doc_length_ls = list()
    # doc_ls = list()
    for i, row in enumerate(rows):
        doc_length_dict[i] = len(row)
        
        doc_length_ls.append(len(row))

    # print("row {}: has length {}".format(list(doc_length_dict)[2], doc_length_dict[2]))
    zipped = zip(rows,doc_length_ls)
    zipped_raw =zip(raw_lines, doc_length_ls)

    sort_doc_byLength = sorted(zipped, key=lambda x: x[1]).copy()
    sort_doc_byLength_raw = sorted(zipped_raw, key=lambda x: x[1]).copy()

    adj_distance_ls = []
    for idx, i in enumerate(sort_doc_byLength):
        if idx +1 == len(sort_doc_byLength):
            continue
        adj_distance_ls.append(abs(i[1] -  sort_doc_byLength[idx+1][1])) 
    
    sort_doc_byLength_unzip = list(zip(*sort_doc_byLength))   
    sort_doc_byLength_unzip_raw = list(zip(*sort_doc_byLength_raw))   
    # print (sort_doc_byLength_unzip[1][:10])
    # print(adj_distance_ls[:10])

    min_len = sort_doc_byLength_unzip[1][0]
    max_len = sort_doc_byLength_unzip[1][-1]
    max_distance = max_len - min_len
    adj_distance_ls.append(max_distance)
    # print('max_distance ', max_distance)
    distance_ls = range(max_distance)
    # print('distance_ls ', len(distance_ls))
    temp_ = [range(len(sort_doc_byLength_unzip[1]))]
    temp = []
    for i in sort_doc_byLength_unzip[1]:
        temp.append([{i:0}])    #nested. Each index is a cluster of 1 element. 

    sort_doc_byLength_unzip.append(temp) # add list of cluster index, nested list and dict
    # sort_doc_byLength_unzip = [(docs ), (docs lenth), [cluster index]]
    # print (sort_doc_byLength_unzip[2][:3])
    
    # merge looop
    for idx, i in enumerate(sort_doc_byLength_unzip[2]):    #first round

        # check current adjaction distance 
        # i = [{length:dist}]
        #update length
        # print(i)
        # print('here')
        # print(sort_doc_byLength_unzip[2][idx][-1].copy().keys())
        temp = tuple(sort_doc_byLength_unzip[2][idx][-1].copy().keys())[0] #get the key of the last
        # print(temp)
        sort_doc_byLength_unzip[2][idx][-1][temp] =  adj_distance_ls[idx]
        # print(sort_doc_byLength_unzip[2][idx][-1])
        # break
        # sort_doc_byLength_unzip[2][idx][i[-1].items()[1]] =  abs(i[-1].items()[1] - sort_doc_byLength_unzip[2][idx +1][0].items()[1])
    # print( adj_distance_ls[:10])
    # print (sort_doc_byLength_unzip[2][:10])
    # print("original lines: ", len(sort_doc_byLength_unzip[2]))
    # merge loop
    while len(sort_doc_byLength_unzip[2]) >3:
        for e in distance_ls:
            # iterator_marks = iter(sort_doc_byLength_unzip[2])
            # the next element is the first element
            # i = next(iterator_marks)
            merge_dist = e
            
            for idx, i in enumerate(sort_doc_byLength_unzip[2]): # all rounds

                # merged = sort_doc_byLength_unzip[2].copy()
                # merge_dist = distance_ls[0]
                
                # print(idx)
                # print (i)
                if merge_dist == tuple(i[-1].values())[0]:
                    # print('merge_dist ', merge_dist)
                    # print('m dist ', tuple(i[-1].values())[0])
                    # print(sort_doc_byLength_unzip[2][idx+1])
                    next_ = sort_doc_byLength_unzip[2][idx+1].copy()
                    sort_doc_byLength_unzip[2].remove(sort_doc_byLength_unzip[2][idx+1])

                    sort_doc_byLength_unzip[2][idx] = sort_doc_byLength_unzip[2][idx] + next_
                    # print('merge')
                # if len(sort_doc_byLength_unzip[2]) <=3:
                #     # print(sort_doc_byLength_unzip[2][:10])
                #     break
            # print(sort_doc_byLength_unzip[2][:10])
            # if len(sort_doc_byLength_unzip[2]) <=3:
            #     # print(sort_doc_byLength_unzip[2][:10])
            #     break
                # # end
                # distance_ls.pop(0)
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
    # print(len(sort_doc_byLength_unzip_raw[0]))
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

    # val = 0. # this is the value where you want the data to appear on the y-axis.
    # ar = np.array(sort_doc_byLength_unzip[1]) # just as an example array
    # plt.plot(ar, np.zeros_like(ar) + val, 'x')
    # plt.show()