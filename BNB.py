#!/usr/bin/python
# -*- coding: UTF-8 -*-

# for generating path using "Branch and Bound"
import numpy as np
import sys
import copy as cp
import graphviz as gv
import Queue as Q
import random
from MST import check
'''
define the direction:
-1 -> item <- 1
'''
direction=1
upper_bound=sys.maxint
can_path=[]
op_path=[]
traverse=[]
weight={}



def bnb(tem,i):
    tem1= cp.copy(tem)
    row = tem1.min(1)
    if(row[i]>50 or i==(len(tem)-1)):
        return sys.maxint
    else:
        for k in range(0,len(tem)):
            tem1[k][i]=sys.maxint
        cur_sum=0
        col = tem1.min(1)
        for i in range(0,len(tem)):
            if(col[i]<50):
                tem1[i]=tem1[i]-col[i]
                cur_sum=cur_sum+col[i]
        row = tem1.min(0)
        for m in range(0,len(tem)):
            for n in range(0,len(tem)):
                if(row[m]<50):
                    tem1[n][m]-=row[m]
            if(row[m]<50):
                cur_sum+=row[m]
        return cur_sum


class Node(object):
    def __init__(self,level,tail,value,matrix , path):
        self.level=level
        self.value = value
        self.tail=tail
        self.matrix=matrix
        self.path=path

        return
    def __cmp__(self, other):
        if(self.value>other.value):
            return True
        elif(self.value<other.value):
            return False
        elif(self.level<other.level):
            return True
        else:
            return False


def cal_distance(x1,x2,y1,y2,direction):
    if(x1<x2):
        if(direction==-1):
            return abs(x2-x1)+abs(y2-y1)
        if(direction==1):
            direction=-1
            return  abs(x2-x1)+abs(y2-y1)-1
    if(x1>x2):
        if(direction==-1):
            direction=1
            return abs(x2-x1)+abs(y2-y1)-1
        if(direction==1):
            return  abs(x2-x1)+abs(y2-y1)-1
    if(x1==x2):
        return abs(y2-y1)
    return 1;


# factor in weight or not
def cal_path_w(list,weight,dict2,dict4):
    num_dict = dict4.copy()
    print dict4
    print num_dict
    now_w=0
    now_dict = dict2.copy()
    x_1=list[0][0]
    y_1=list[0][1]
    print "BNB"
    print "If weight in factor, the path will be: "
    print"(",x_1,",",y_1,")->",
    tem_list = []
    tem_list.append(0)
    s=''
    s1=0
    select=""
    for i in range(1,len(list)-1):
        for key in now_dict:
            if(now_dict[key][0]==list[i][0] and now_dict[key][1]==list[i][1]):
                select=key
                s=num_dict[key]
                s1=int(s)
                tem_list.append(s1)
        now_dict.pop(select)
        num_dict.pop(select)

    for i in range(1,len(list)):
        x_2=list[i][0]
        y_2=list[i][1]
        tem_w = 0
        print"now we will use ", dict4[i],
        try:
            tem_w=weight[dict4[i]]
        except KeyError:
            tem_w=0
            print "(weight missing! )",
        print"(",x_2,",",y_2,")->",
        now_w = (abs(x_1-x_2)+abs(y_1-y_2))*tem_w
        x_1=x_2
        y_1=y_2

    print "END"
    print "The total effort is :", now_w


def cal_path_nw(list):
    nw_length=0
    x_1=list[0][0]
    y_1=list[0][1]
    print "BNB"
    print "If weight not in factor, the path will be: "
    print"(",x_1,",",y_1,")->",
    for i in range(1,len(list)):
        x_2=list[i][0]
        y_2=list[i][1]
        nw_length+=abs(x_1-x_2)+abs(y_1-y_2)
        x_1=x_2
        y_1=y_2
        print"(",x_2,",",y_2,")->",
    print "END"
    print "The total cost with B&B will be:", nw_length


# 根据reduced matrix选择路径，不改变原来的matrix
def init_first_row(tem,i,Node):
    tem1= cp.copy(tem)
    row = tem1.min(1)
    sel = i
    if(row[i]>50 or i==(len(tem)-1)):
        return sys.maxint
    else:
        for k in range(0,len(tem)):
            tem1[k][i]=sys.maxint
        cur_sum=0
        col = tem1.min(1)
        for i in range(0,len(tem)):
            if(col[i]<50):
                tem1[i]=tem1[i]-col[i]
                cur_sum=cur_sum+col[i]
        row = tem1.min(0)
        for m in range(0,len(tem)):
            for n in range(0,len(tem)):
                if(row[m]<50):
                    tem1[n][m]-=row[m]
                    cur_sum=cur_sum+row[m]
        tem1[sel]=sys.maxint
        Node.value+=cur_sum
        Node.matrix=tem1

def find_path(Node,list):
    sum=0
    short = sys.maxint
    cur=0
    for i in range(0,len(list)):
        sum=bnb(Node.matrix, i)
        if(sum<short and sum<50):
            short=sum
            cur=i
    Node.value+=short
    Node.level+=1
    Node.matrix[cur]=sys.maxint
    Node.tail=cur
    Node.path.append(list[Node.tail])
    #print "value is :", Node.value
    #print "path:", Node.path
    #print "mat"
    #print Node.matrix



#之前的主程序
def branch(dict2,weight_dict,start_point,end_point,w,dict4):
    # store the distance matrix
    dict=dict2.copy()
    weight=weight_dict.copy()
    # there can't be same spot to calculate the mst using this method
    dict=check(dict)
    list=[]

    # input information from main function
    node = []
    node.append(start_point[0])
    node.append(start_point[1])
    list.append(node)
    for key in dict:
        node = []
        node.append(dict[key][0])
        node.append(dict[key][1])
        list.append(node)
    node = []
    node.append(end_point[0])
    node.append(end_point[1])

    # 这里的list包含了所有的点
    list.append(node)
    #如果只有一个item，那就无需规划了
    if(len(list)==3):
        if(w=="y"):
            cal_path_w(list,weight,dict2,dict4)
        else:
            cal_path_nw(list)

    list2= cp.copy(list)
    # build the matrix with the list
    mat = []
    for i in range(0,len(list)):
        dis=[]
        for j in range(0,len(list)):
            if(i==j):
                dis.append(sys.maxint)
            else:
                #dis.append(cal_distance(list[i][0],list[j][0],list[i][1],list[j][1],direction))
                dis.append(abs(list[i][0]-list[j][0])+abs(list[i][1]-list[j][1]))
        mat.append(dis)
    a = np.array(mat)
    #这里的a就是所有的矩阵
    # firstly, get the lower bound using the initial reduced matrix
    # generate the optimal path generated by bnb
    pathbnb = []
    # the initial reduced matrix cost
    init_sum=0
    col = a.min(1)
    for i in range(0,len(a)):
        a[i]=a[i]-col[i]
        init_sum=init_sum+col[i]
    row = a.min(0)
    for m in range(0,len(a)):
        for n in range(0,len(a)):
            a[n][m]-=row[m]
            init_sum=init_sum+row[m]
    #这里的a是reduced matrix
    #init_sum 就是初始reduced的值，选择路径时不考虑进去
    # nodes initialization
    a[0]=sys.maxint
    q = Q.PriorityQueue()
    for i in range(1,len(list)-1):
        temp=[]
        temp.append(list[0])
        temp.append(list[i])
        tem_lv=1
        tem_tail = i
        curNode = Node(tem_lv,0,tem_tail,a,temp)
        init_first_row(a,i,curNode)
        #print "lv ", curNode.level, " value ", curNode.value," paht ", curNode.path
        #print "mat"
        #print  curNode.matrix
        q.put(curNode)


    while not q.empty():
        global upper_bound
        n=q.get()
        if(n.value>=upper_bound):
            continue
        else:
            if q.empty():
                break
            else:
                if(len(n.path)==len(list)-1):
                    m=q.queue[0]
                    if(m.value>=n.value):
                        op_path=n.path
                        break
                    else:
                        if(upper_bound>n.value):
                            upper_bound=n.value
                            can_path=n.path
                find_path(n,list)
                q.put(n)
    if(len(op_path)==0):
        op_path=can_path
    op_path.append(end_point)
    if(w=="y"):
        cal_path_w(op_path,weight,dict2,dict4)
    else:
        cal_path_nw(op_path)


#while not q.empty():
    #best =  q.get()
    #print "lv ", Node.level, " value ", Node.value," paht ", Node.path
    #print "mat"
    #print  Node.matrix





