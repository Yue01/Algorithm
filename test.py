'''
warehouse-orders-5item.csv

'''


import sys
import numpy as np

direction1 = 1
direction2=-1

def cal_distance(x1,x2,y1,y2,direction1,direction2):
    if(x1<x2):
        if(direction1==-1):
            return abs(x2-x1)+abs(y2-y1)
        if(direction1==1):
            return abs(x2-x1)+abs(y2-y1)
    elif(x1>x2):
        if(direction1==-1):
            return abs(x2-x1)+abs(y2-y1)
        if(direction1==1):
            return abs(x2-x1)+abs(y2-y1)
    else:
        return abs(x2-x1)+abs(y2-y1)


list = [[0, 0], [7, 7], [10, 10]]
append_list = []
append_list.append(list[0])
for i in range(1,len(list)-1):
    lx=list[i][0]*2-1
    ly=list[i][1]*2
    append_list.append([lx,ly])
    rx=list[i][0]*2+1
    ry=list[i][1]*2
    append_list.append([rx,ry])
end_cur = len(list)-1
rx=list[end_cur][0]*2-1
ry=list[end_cur][1]*2
append_list.append([rx,ry])
print "the current list: "
print append_list

mat = []
for i in range(0,len(append_list)):
    dis=[]
    for j in range(0,len(append_list)):
        if(i==j):
            dis.append(sys.maxint)
        elif(i%2==1 and j==i+1 ):
            dis.append(sys.maxint)
        elif(i%2==0 and j==i-1 and i>0):
            dis.append(sys.maxint)
        else:
            if(i%2==0):
                direction1==1
            else:
                direction1==-1
            if(j%2==0):
                direction2==1
            else:
                direction2==-1
            dis.append(cal_distance(append_list[i][0],append_list[j][0],append_list[i][1],append_list[j][1],direction1,direction2))
            #dis.append(abs(append_list[i][0]-append_list[j][0])+abs(append_list[i][1]-append_list[j][1]))
    mat.append(dis)
print mat
a = np.array(mat)
print a

for i in range(0,4):
    print i

