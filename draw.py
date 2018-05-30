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
    print dict




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
            # while not queue.empty():
            #     cur = queue.get()
            #     print cur.list
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
