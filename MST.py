#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import sys

# add start/end point
def append(dict, point, sum):
    distance =sys.maxint
    for key in dict:
        tem = dict[key]
        curx = tem[0]
        cury = tem[1]
        curd = abs(point[0]-curx)+abs(point[1]-cury)
        if(curd<=distance):
            distance=curd
        #print distance
    return distance

def check(dic):
    res={}
    count=0
    check_list=[]
    exist = False
    for key in dic:
        x=dic[key][0]
        y=dic[key][1]
        for i in range(0,len(check_list)):
            if check_list[i][0]==x and check_list[i][1]==y:
                exist = True
        if not exist:
            check_list.append([x,y])
        exist=False
    for j in range(0,len(check_list)):
        res[count]=check_list[j]
        count=count+1
    return res

def generatemst(dict2,start_point,end_point):
    # store the distance matrix
    dict=dict2.copy()
    # there can't be same spot to calculate the mst using this method
    dict = check(dict)
    print dict
    v=[]
    dict[len(dict)]=start_point
    dict[len(dict)]=end_point
    for i in range(0,len(dict)):
        v1=[]
        for j in range(0,len(dict)):
            if(j<=i):
                v1.append(0)
            else:
                x=0
                x=abs(dict[i][0]-dict[j][0])+abs(dict[i][1]-dict[j][1])
                v1.append(x)
        v.append(v1)
    Tcsr = minimum_spanning_tree(csr_matrix(v))
    print("2. The Minimum Spanning Tree: ")
    print v
    Tcsr=str(Tcsr).split()
    counter=0
    tem=0
    sum=0
    for i in range(len(Tcsr)):
        if(counter==2):
            tem=int(float(Tcsr[i]))
            sum=sum+tem
            counter=0
        else:
            counter+=1
    #sum+=append(dict,start_point,sum)
    #sum+=append(dict,end_point,sum)
    print("3. The total path of minimum spanning tree is : ")
    print sum


