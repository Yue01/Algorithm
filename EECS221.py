#!/usr/bin/python
# -*- coding: UTF-8 -*-
#from MST import generatemst
import random
import copy
import csv
import sys
import time
import graphviz as gv
from BNB import branch
import Queue as Q
from BNB import BNB_reset

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import ttk
import pickle
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from draw import draw_graph
from draw import draw_reset
from BNB import check




class Item(object):
    def __init__(self,list):
        self.list=list
        return
    def __cmp__(self, other):
        if(self.list[0]>other.list[0]):
            return True
        else:
            return False
#original path length
origin=0
opt=0
order_name=""
start_point=[0,0]
end_point=[0,0]
choice = 'n'
w='n'
added_flag = 0
canvas_list=[]
all_order_list=[]
res_list=[]
current_total_weight=0
default_weight=0
queue = Q.PriorityQueue()
status = {}
read_line_counter=0



# to define left or right in NN:
direction = 1

# use a dictionary to save all the nodes
dict={}  # for all the items
dict_w={} # for weight information
orderdict={} # for all the orders

def set_al():
    global choice
    choice = 'b'
def set_al_1():
    global choice
    choice = 'n'

def set_weight():
    global w
    w='y'
def set_weight_2():
    global w
    w='n'

def read_latest():
    global res_list
    global choice
    global w
    global default_weight
    global start_point
    global end_point
    global status
    status = {}
    read_in_list=[]
    if(str(numberChosen.get())=="NN with weight"):
        pickle_in = open("nn_w.pickle","r")
        choice="n"
        w='y'
    elif(str(numberChosen.get())=="NN without weight"):
        pickle_in = open("nn.pickle","r")
        choice="n"
        w='n'
    elif(str(numberChosen.get())=="B&B with weight"):
        pickle_in = open("bb_w.pickle","r")
        choice = "b"
        w='y'
    elif(str(numberChosen.get())=="B&B without weight"):
        pickle_in = open("bb.pickle","r")
        choice = "b"
        w='n'
    read_in_list = pickle.load(pickle_in)
    default_weight = read_in_list[0][6]
    start_point[0]=read_in_list[0][2]
    start_point[1]=read_in_list[0][3]
    end_point[0]=read_in_list[0][4]
    end_point[1]=read_in_list[0][5]
    print str(numberChosen.get()),",start:(",str(start_point[0]),",",str(start_point[1]),"),end:(",str(end_point[0]),",",str(end_point[1]),"),Max weight:",str(default_weight)
    status = read_in_list[1]
    res_list = read_in_list[2]
    num_of_res.set(len(res_list))



def reset_para():
    global current_total_weight
    global queue
    global canvas_list
    global default_weight
    global added_flag
    current_total_weight=0
    queue=Q.PriorityQueue()
    canvas_list=[]
    BNB_reset()
    draw_reset()
    added_flag = 0
    # default_weight=0
#the start button activity in GUI
def hit_me():
    global canvas_list
    global order_name
    global start_point
    global end_point
    global current_total_weight
    global choice
    global w
    global status
    global read_line_counter
    global res_list
    status={}
    canvas_list=[]
    maxw = int(w_qwer.get())
    start_point[0]=int(s_x.get())
    start_point[1]=int(s_y.get())
    end_point[0]=int(e_x.get())
    end_point[1]=int(e_y.get())
    read_line_counter=0
    #order_name=str(numberChosen.get())
    with open('warehouse-orders-v02-tabbed.txt', 'r') as file:
        res_list=[]
        read = file.readline()
        cur_order_weight=0
        while not (read==""):
            if not read:
                break
            print "Orders so far："
            print read_line_counter
            cur_order_weight=0
            read_line_counter+=1
            cur_list=[]
            order = read.split()
    # To professor:
    # Here I am confused that I can get the weight from the dictionary dict_w but almost all the itemid in "weight" and "item" don't match
    # For example, I looked up all the ids in the first 20 order (in the updated file), only 2 of the items show up in "weight" file
    # as a result, almost all the nodes show: "weight missing" (when the weight is a factor), for which I don't think this makes sense
    # So to prove that my algorithm really works: give them the default value,and use this for batch processing
            if(w=="y"):
                # if we factor in weight: the max weight is the input and I define that the maximum # of items in a single order is 8
                for i in range (0,len(order)):
                    #tem_w = dict_w[order[i]]
                    tem_w = 2
                    cur_order_weight+=tem_w
                    cur_list.append(order[i])
                if cur_order_weight<maxw:
                    status[read_line_counter]="Combined and split!"
                    while cur_order_weight<maxw:
                        read = file.readline()
                        order = read.split()
                        for i in range (0,len(order)):
                            #tem_w = dict_w[order[i]]
                            tem_w = 2
                            cur_order_weight+=tem_w
                            cur_list.append(order[i])
                elif(cur_order_weight>maxw):
                    status[read_line_counter]="Big order:Split!"
                else:
                    status[read_line_counter]="Just fine!"

                cur_order_list=[]
                new_split_list = []
                max_weight = int(w_qwer.get())
                sum_weight =0

                for i in range(len(cur_list)):
                    #tem_w = dict_w[order[i]]
                    tem_w = 2
                    if sum_weight+tem_w>maxw:
                        res_dict=singleorder(new_split_list)
                        cur_order_list.append(res_dict)
                        new_split_list=[]
                        new_split_list.append(cur_list[i])
                        sum_weight = tem_w
                    else:
                        new_split_list.append(cur_list[i])
                        sum_weight+=tem_w
                if not (len(new_split_list)==0):
                    res_dict=singleorder(new_split_list)
                    cur_order_list.append(res_dict)
                res_list.append(cur_order_list)
                read = file.readline()
            else:
                # if weight not in factor: just let it forward
                cur_order_list=[]
                res_dict=singleorder(order)
                cur_order_list.append(res_dict)
                res_list.append(cur_order_list)
                read = file.readline()
    file.close()
    num_of_res.set(len(res_list))
    print "done!!"

    # save in the batch file
    save_res_list=[]
    condition = []
    if(choice=='b'):
        condition.append("b")
    else:
        condition.append("n")
    if(w=='n'):
        condition.append("n")
    if(w=='y'):
        condition.append("y")
    condition.append(start_point[0])
    condition.append(start_point[1])
    condition.append(end_point[0])
    condition.append(end_point[1])
    condition.append(int(w_qwer.get()))
    save_res_list.append(condition)
    save_res_list.append(status)
    save_res_list.append(res_list)
    if(w=='y'):
        if(choice=='b'):
            pickle_out = open("bb_w.pickle","w")
        else:
            pickle_out = open("nn_w.pickle","w")
    elif(w=='n'):
        if(choice=='b'):
            pickle_out = open("bb.pickle","w")
        else:
            pickle_out = open("nn.pickle","w")
    pickle.dump(save_res_list,pickle_out)
    pickle_out.close()


def process():
    print "In this order:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    global canvas_list
    global res_list
    global added_flag
    num_order=int(choose_input.get())
    if w=="y":
        fd.set(status[num_order])
    else:
        fd.set("No weight!")
    canvas_list = res_list[num_order-1]
    draw_graph(canvas_list,w)


# used for data transfer
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
# prepossessing data file for the nodes
with open('warehouse-grid.csv', 'r') as file:
    read = csv.DictReader(file)
    for row in read:
        pos = [0,0]
        item=row['itemnum']
        pos[0]=int(float(row['x']))
        pos[1]=int(float(row['y']))
        dict[item]=pos
file.close()

with open('item-dimensions-tabbed.txt', 'r') as file:
    read = file.readline()
    while not (read==""):
        if not read:
            break
        numbers = read.split()
        n=str(numbers[0])
        n1= int(n)
        m=numbers[4]
        m_1=num(m)
        dict_w[n1]=m_1
        read = file.readline()
file.close()
with open('warehouse-orders-v02-tabbed.txt', 'r') as file:
    read = file.readline()
    while not (read==""):
        if not read:
            break
        order = read.split()
        all_order_list.append(order)
        read = file.readline()
file.close()


'''
start_time = time.time()  # remember when we started
while (time.time() - start_time) < max_time:
    do_stuff()
'''

# functions
def get_dis(x1,y1,x2,y2):
    global direction
    if(x1<x2):
        if(direction==1):
            direction=-1
            return abs(x2-x1-2)+abs(y2-y1)
        else:
            return abs(x2-x1)+abs(y2-y1)
    elif(x1>x2):
        if(direction==1):
            return abs(x2-x1)+abs(y2-y1)
        else:
            direction=1
            return abs(x2-x1-2)+abs(y2-y1)
    else:
        return abs(y2-y1)



# original path length
def original(order):
    origin=0
    startx = start_point[0]
    starty = start_point[1]
    endx=end_point[0]*2
    endy=end_point[1]*2
    for i in range(0,len(order)):
        place = dict[order[i]]
        origin=origin+abs(place[0]*2-startx*2)+abs(place[1]*2-starty*2)
        startx=place[0]*2
        starty=place[1]*2
    origin=origin+abs(endx-startx)+abs(endy-starty)
    print("1. The orginal path length is : "),
    print origin

# for a single order:
def singleorder(order):
    global direction
    # the optimimal path length
    opt_final=sys.maxint
    pathlist_final=[]
    #from the start: initialization
    dict1={}
    dict2={}
    dict5={}


    #put all nodes in this dictionary
    for i in range(0,len(order)):
        place = dict[order[i]]
        # dict5 用来存放order number
        dict5[i]=order[i]
        dict1[i]=place
    dict1 = check(dict1)
    dict2=copy.deepcopy(dict1)

    if(choice=="b"):
        return branch(dict2,dict_w,start_point,end_point,w,dict5)
    # improvement for nearest neighbour
    opt=0
    curd=0
    pathlist=[]
    dict3={}
    dict3=copy.deepcopy(dict1)


    startx = start_point[0]
    starty = start_point[1]
    endx=end_point[0]
    endy=end_point[1]


    while (len(dict3)>0):
        distance =sys.maxint
        for key in dict3:
            tem = dict3[key]
            curx = tem[0]
            cury = tem[1]
            curd = abs(startx-curx)+abs(starty-cury)
            if(curd<distance):
                distance=curd
                next=key
        pathlist.append(next)
        opt+=distance
        node = dict3[next]
        startx=node[0]
        starty=node[1]
        dict3.pop(next)
    opt=0
    # print("Here is the optimal path:")
    # if(w=="n"):
    opt=0
    total_weight = 0
    effort = 0
    direction =1
    temp_dict={}
    info=[]
    # print("("),
    # print(start_point[0]*2),
    startx=start_point[0]*2
    # print(","),
    # print(start_point[1]*2),
    starty=start_point[1]*2
    info.append(0)
    info.append(startx)
    info.append(starty)
    temp_dict[0]=info
    # print(")->"),
    for i in range(len(pathlist)):
        info=[]
        col = dict2[pathlist[i]]
        cur_path = get_dis(startx,starty,col[0]*2,col[1]*2)
        opt+=cur_path
        #opt=opt+abs(col[0]*2-startx)+abs(col[1]*2-starty)
        startx=col[0]*2
        starty=col[1]*2
    #     try:
    #         weight = dict_w[key]
    #         total_weight+=tem_w
    #         print "(weight: ",tem_w," )",
    #     except KeyError:
    #         tem_w=0
    #         print "(weight missing! )",
        tem_w =2
        effort +=cur_path*total_weight
        total_weight+=tem_w
        info.append(tem_w)
        info.append(startx+direction)
        info.append(starty)
        temp_dict[i+1]=info
        # print("("),
        # print(col[0]*2),
        # print(","),
        # print(col[1]*2),
        # print(")->"),
    endx=end_point[0]*2
    endy=end_point[1]*2
    last_path = get_dis(startx,starty,endx,endy)
    opt+=last_path
    info=[]
    info.append(0)
    info.append(endx+direction)
    info.append(endy)
    effort +=last_path*total_weight
    temp_dict[len(pathlist)+1]=info
    # print("("),
    # print(end_point[0]*2),
    # print(","),
    # print(end_point[1]*2),
    # print(")->"),
    # print("END")
    # print("The optimal path length is : "),
    # print opt
    # if(w=="y"):
    #     print "The total effort in this order is :", effort
    # print("\n")
    return temp_dict


# for all orders
def allorder(order_name):
    with open(order_name, 'r') as f:
        read = csv.reader(f)
        all = list(read)
        for i in range(len(all)):
            each = str(all[i])[2:-2]
            order = each.split()
            # first calculate the distance that the original order covers
            original(order)
            # then with the optimal path
            singleorder(order)

    f.close()



win = tk.Tk()
var1= tk.StringVar()
var2 = tk.StringVar()
win.title('EECS221A App')
win.geometry('220x525')


all = Frame(win)
all.pack(side="top")
left = Frame(all,borderwidth=5,bg='white')
left.pack(side="left")
right = Frame(all)
right.pack(side="right")

algorithm = Frame(left,bg='white')
algorithm.pack(side = "top")
al_select = Frame(left,bg='white')
al_select.pack(side = "top")

p1=tk.Label(left, width=20, text='2.Start point:',bg='white')
p1.pack(side="top")
point1= Frame(left)
point1.pack(side = "top")
p2=tk.Label(left, width=20, text='3.End point:',bg='white')
p2.pack(side="top")
point2= Frame(left)
point2.pack(side = "top")

w=tk.Label(left, width=20, text='4.Factor in weight?',bg='white')
w.pack(side="top")
weight = Frame(left)
weight.pack(side = "top")
ws=tk.Label(left, width=20, text='5.If yes, input max weight:',bg='white')
ws.pack(side="top")
w_select = Frame(left)
w_select.pack(side = "top")

# f=tk.Label(left, width=20, text='6.Which file to process?',bg='white')
# f.pack(side="top")
file= Frame(left)
file.pack(side = "top")
rs=tk.Label(left, width=20, text='6.Results in the batch file',bg='white')
rs.pack(side="top")
res_show = Frame(left)
res_show.pack(side="top")
end= Frame(right)
end.pack(side = "top")

bottomframe = Frame(left)
bottomframe.pack( side = "top" )
# now it's time to draw
ch=tk.Label(left, width=20, text='7.Show one of the result:',bg='white')
ch.pack(side="top")
fd = tk.StringVar()
feedback = tk.Label(left, textvariable=fd, bg='grey', font=('Arial', 8), width=15,
             height=2)
feedback.pack(side="top")
choose = Frame(left)
choose.pack(side="top")
ch=tk.Label(left, width=20, text='8.Use latest result:',bg='white')
ch.pack(side="top")
number = tk.StringVar()
numberChosen = ttk.Combobox(left, width=22, textvariable=number)
numberChosen['values'] = ("NN with weight", "NN without weight", "B&B with weight", "B&B without weight")
numberChosen.pack(side = "top")

numberChosen.current(0)
other_op=Frame(left)
other_op.pack(side="top")

# first title
l = tk.Label(algorithm,width=20, text='1.Algorithm',bg='white')
l.pack(side="top")
# selection
r1 = tk.Radiobutton(al_select,text='Nearest Neighbor',
                    variable=var1, bg='white',value='n',command  = set_al_1)
r1.pack(side="top")
r2 = tk.Radiobutton(al_select,text='Branch and Bound',
                    variable=var1, bg='white',value='b',command = set_al)
r2.pack(side="top")
#inserting points
s_x = tk.Entry(point1,width=6)
s_x.grid(row=1,column=1)

s_y=tk.Entry(point1,width=6)
s_y.grid(row=1,column=3)

e_x = tk.Entry(point2,width=6)
e_x.pack(side="left")

e_y=tk.Entry(point2,width=6)
e_y.pack(side="left")
# factor in weight or not:
w_1 = tk.Radiobutton(weight,text='Yes',
                    variable=var2, bg='white',value='y',command =set_weight)
w_1.pack(side="left")
w_2 = tk.Radiobutton(weight,text='No',
                    variable=var2,bg='white',value='n',command = set_weight_2)
w_2.pack(side="left")
# input max weight:
l = tk.Label(w_select,width=5, text='max:',bg='white')
l.pack(side="left")

w_qwer=tk.Entry(w_select,width=5)
w_qwer.pack(side="left")
dw = tk.Label(w_select,width=5, text='(kg)',bg='white')
dw.pack(side="left")

# to show the information
num_of_res = tk.StringVar()
nos = tk.Label(res_show, textvariable=num_of_res, bg='grey', font=('Arial', 8), width=15,
             height=2)
nos.pack(side="top")
# at the end:
b = tk.Button(bottomframe, text='Start', width=5,
              height=1, command=hit_me)
b.grid(row=3,column=1)
choose_input = tk.Entry(choose,width=3)
choose_input.pack(side="left")

# draw = tk.Button(choose, text='Add', width=4,
#               height=1, command=add_order)
# draw.pack(side="left")
go_button = tk.Button(choose, text='Go!', width=3,
              height=1, command=process)
go_button.pack(side="left")
# latest = tk.Button(other_op, text='Latest', width=5,
#               height=1, command=read_latest)
# latest.pack(side="top")
read = tk.Button(other_op, text='Read', width=5,
              height=1, command=read_latest)
read.pack(side="left")
reset = tk.Button(other_op, text='Reset', width=5,
              height=1, command=reset_para)
reset.pack(side="left")

win.mainloop()


