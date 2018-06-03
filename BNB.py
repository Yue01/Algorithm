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
direction1=1
direction2=1
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

def BNB_reset():
    global op_path
    global upper_bound
    global can_path
    global  traverse
    upper_bound=sys.maxint
    can_path=[]
    op_path=[]
    traverse=[]
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


# factor in weight or not
def cal_path_w(list,weight,dict2,dict4):
    # used to store the nodes information
    temp_dict={}
    # info: [weight, x, y]
    info=[]
    #dict4: [key, itemnum]
    #weight:[itemnum, weight]
    #dict2[key, position]
    num_dict = dict4.copy()

    effort = 0
    total_w=0
    nw_length = 0
    now_dict = dict2.copy()
    x_1=list[0][0]
    y_1=list[0][1]
    info.append(0)
    info.append(x_1)
    info.append(y_1)
    temp_dict[0]=info
    # print "Here is the optimal path: "
    # print"(",x_1,",",y_1,")->",
    tem_list = []
    tem_list.append(0)
    s=''
    s1=0
    select=""
    for i in range(1,len(list)-1):
        for key in now_dict:
            if((now_dict[key][0]-list[i][0])<=1 and now_dict[key][1]*2==list[i][1]):
                select=key
                s=num_dict[key]
                s1=int(s)
                tem_list.append(s1)
        try:
            now_dict.pop(select)
            num_dict.pop(select)
        except KeyError:
            print ""

    for i in range(1,len(list)-1):
        x_2=list[i][0]
        y_2=list[i][1]
        tem_w = 0
        try:
            #tem_w=weight[dict4[i]]
            tem_w=2
        except KeyError:
            tem_w=2
            print "(weight missing! )",
        info=[]
        info.append(tem_w)
        info.append(x_2)
        info.append(y_2)
        temp_dict[i]=info
        # print"(",x_2,",",y_2,")->",
        nw_length += (abs(x_1-x_2)+abs(y_1-y_2))
        effort =total_w*(abs(x_1-x_2)+abs(y_1-y_2))
        total_w+=tem_w
        x_1=x_2
        y_1=y_2
    x_2=list[len(list)-1][0]
    y_2=list[len(list)-1][1]
    nw_length += (abs(x_1-x_2)+abs(y_1-y_2))
    effort =total_w*(abs(x_1-x_2)+abs(y_1-y_2))
    info=[]
    info.append(0)
    info.append(list[len(list)-1][0])
    info.append(list[len(list)-1][1])
    temp_dict[len(list)-1]=info
    # print "END"
    # print("The optimal path length is : "),nw_length
    # print "The total effort in this order is :", effort
    return temp_dict



def cal_path_nw(list):
    temp_dict={}
    info=[]
    nw_length=0
    x_1=list[0][0]
    y_1=list[0][1]
    info.append(0)
    info.append(x_1)
    info.append(y_1)
    temp_dict[0]=info
    # print "Here is the optimal path: "
    # print"(",x_1,",",y_1,")->",
    for i in range(1,len(list)):
        info=[]
        x_2=list[i][0]
        y_2=list[i][1]
        nw_length+=abs(x_1-x_2)+abs(y_1-y_2)
        x_1=x_2
        y_1=y_2
        info.append(0)
        info.append(x_2)
        info.append(y_2)
        temp_dict[i]=info
    #     print"(",x_2,",",y_2,")->",
    #
    # print "END"
    # print("The optimal path length is : "),nw_length
    return temp_dict


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
        if(sel%2==0 and not sel==0):
            tem1[sel]=sys.maxint
            tem1[sel-1]=sys.maxint
        elif(sel%2==1 and not sel==(len(tem)-1)):
            tem1[sel]=sys.maxint
            tem1[sel+1]=sys.maxint
        Node.value+=cur_sum
        Node.matrix=tem1
        # print "Matrix is :"
        # print Node.matrix
        # print "value is "
        # print Node.value
        # print "the current path si :"
        # print Node.path

def find_path(Node,append_list):
    sum=0
    short = sys.maxint
    cur=0
    for i in range(0,len(append_list)):
        sum=bnb(Node.matrix, i)
        if(sum<short and sum<60):
            short=sum
            cur=i
    if(short>300):
        short= 300
    Node.value+=short
    Node.level+=1
    if(cur%2==0 and not cur==0):
        Node.matrix[cur]=sys.maxint
        Node.matrix[cur-1]=sys.maxint
    elif(cur%2==1 and not cur==(len(append_list)-1)):
        Node.matrix[cur]=sys.maxint
        Node.matrix[cur+1]=sys.maxint
    Node.tail=cur
    Node.path.append(append_list[Node.tail])




#之前的主程序
def branch(dict2,weight_dict,start_point,end_point,w,dict4):
    global op_path
    global upper_bound
    upper_bound=sys.maxint
    # store the distance matrix
    dict=cp.deepcopy(dict2)
    weight=weight_dict.copy()
    # there can't be same spot to calculate the mst using this method
    cal_dict = cp.deepcopy(dict)
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

    list2= cp.copy(list)

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
    #append list include all the nodes: with start and end
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
    for i in range(1,len(append_list)-1):
        temp=[]
        temp.append(append_list[0])
        temp.append(append_list[i])
        tem_lv=1
        tem_tail = i
        curNode = Node(tem_lv,0,tem_tail,a,temp)
        init_first_row(a,i,curNode)
        # print "initinitinitinit"
        # print "lv ", curNode.level, " value ", curNode.value," path ", curNode.path
        # print "mat"
        q.put(curNode)
    op_path=[]
    while not q.empty():
        n=q.get()
        if(n.value>=upper_bound):
            break
        else:
            if(len(n.path)==len(list)-1):
                if(upper_bound>500):
                    upper_bound=n.value
                    can_path=n.path
                    continue
                else:
                    op_path=n.path
                    break
            else:
                find_path(n,append_list)
                q.put(n)

    if(len(op_path)==0):
        op_path=can_path
    op_path.append(append_list[len(append_list)-1])
    if(w=="y"):
        return cal_path_w(op_path,weight,dict2,dict4)
    else:
        return cal_path_nw(op_path)







