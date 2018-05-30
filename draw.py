#!/usr/bin/python
# -*- coding: UTF-8 -*-
#from MST import generatemst
import random
import copy
import csv
import sys
import time
import Queue as Q
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import ttk
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


sx= 0
sum = 0
queue = Q.PriorityQueue()
class item(object):
    def __init__(self,list):
        self.list=list
        return
    def __cmp__(self, other):
        if(self.list[0]>other.list[0]):
            return True
        else:
            return False


# if without weight:
def draw_without_w(dict):
    root = tk.Tk()
    root.title('EECS221A App')
    root.geometry('320x450')
    f = Figure(figsize=(3, 3.5), dpi=100)
    a = f.add_subplot(111)
    a.set_axis_off()
    plt.xlim(-1,21)
    plt.ylim(-1,21)
    for i in range(1,11):
        for j in range(1,11):
            a.plot(2*i,2*j,'go')
    for key in dict:
        if key==0:
            startx = dict[key][1]
            starty=dict[key][2]
            a.plot(startx,starty,'ro')
        else:
            a.plot(dict[key][1],dict[key][2],'ro')
            a.plot([dict[key][1],startx],[dict[key][2],starty],'k')
            startx = dict[key][1]
            starty=dict[key][2]

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", expand=1)
    go_button = tk.Button(root, text='Quit!', width=3,
              height=1, command=root.destroy)
    go_button.pack(side="top")
    root.mainloop()




#if with weight in factor:
def draw_with_w():
    print "lol"






#firstly, decide whether or not to receive more order

# won:weight? or not?
def receive(can_dict,max,w_o_n):
    global queue
    global sum
    if w_o_n == "y":
        dict = {}
        dict=copy.deepcopy(can_dict)
        for key in dict:
            cur= dict[key][0]
            if not cur==0:
                sum+=cur
                new_item=item(dict[key])
                queue.put(new_item)
        if sum<max:
            return "Can still add more!"
        else:
            return "It's full!"
    else:
        dict=copy.deepcopy(can_dict)
        draw_without_w(dict)
        return "processed!"


def original_start(list1,list2):
    global queue
    global sx
    new_item_1=item(list1)
    sx=list1[1]
    new_item_2=item(list2)
    queue.put(new_item_1)
    queue.put(new_item_2)
    draw_with_w()
    return "processed!"

# def draw_result(can_dict,max):
#     dict = copy.deepcopy(can_dict)
#     root = tk.Tk()
#     # var1= tk.StringVar()
#     # var2 = tk.StringVar()
#     root.title('Result')
#     root.geometry('500x500')
#     sum=0
#     queue = Q.PriorityQueue()
#     for key in dict:
#         cur= dict[key][0]
#         sum+=cur
#         new_item=item(dict[key])
#         queue.put(new_item)
#     # if the total weight < max weight
#     if(sum<=max):
#         print "The order is not splitted!"
#     while not queue.empty():
#         cur = queue.get()
#         print cur.list
