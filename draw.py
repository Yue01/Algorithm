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


class Item(object):
    def __init__(self,list):
        self.list=list
        return
    def __cmp__(self, other):
        if(self.list[0]>other.list[0]):
            return True
        else:
            return False

def draw_reset():
    global sx
    global sum
    global queue
    sx= 0
    sum = 0
    queue = Q.PriorityQueue()

# if without weight:
def draw_graph(list,weight_flag):
    w= weight_flag
    length = 0
    total_weight = 0
    effort=0
    startx=0
    starty=0
    x1=0
    x2=0
    y1=0
    y2=0
    dict={}
    root = tk.Tk()

    for i in range(0,len(list)):
        length=0
        effort=0
        total_weight=0
        top = Toplevel()
        top.title('#'+str(i+1))
        top.wm_geometry("200x300")
        dict=list[i]
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
                print "(", str(startx),",",str(starty),")->",
            else:
                a.plot(int(dict[key][1]),int(dict[key][2]),'ro')
                #[startx,dict[key][1]],[starty,dict[key][2]]
                #a.plot([dict[key][1],startx],[dict[key][2],starty],'k')
                x1=startx
                x2=int(dict[key][1])
                y1=starty
                y2=int(dict[key][2])
                print "(", str(x2),",",str(y2),")->",
                cur_w = dict[key][0]
                effort = (abs(x2-x1)+abs(y2-y1))*total_weight
                total_weight+=cur_w
                length+=(abs(x2-x1)+abs(y2-y1))
                if x1==x2:
                    if not y1==y2:
                        # a.plot([x1, x2],[y1, y2],'k')
                        #ax.arrow(x1, x2, y1, y2, head_width=0.02, head_length=0.02, fc='k', ec='k')
                        a.arrow(x1,y1,x2-x1,y2-y1,head_width=0.6,head_length=0.1)
                elif y1==y2:
                    if not x1==x2:
                        # a.plot([x1, x1],[y1, y1+1],'k')
                        # a.plot([x1, x2],[y1+1, y2+1],'k')
                        # a.plot([x2, x2],[y2+1, y2],'k')
                        # ax.arrow(x1, x1, y1, y1+1, head_width=0.01, head_length=0.02, fc='k', ec='k')
                        # ax.arrow(x1, x2, y1+1, y2+1, head_width=0.01, head_length=0.02, fc='k', ec='k')
                        # ax.arrow(x2, x2, y2+1, y2, head_width=0.01, head_length=0.02, fc='k', ec='k')
                        a.arrow(x1,y1,0,1,head_width=0.6,head_length=0.3)
                        a.arrow(x1,y1+1,x2-x1,y2-y1,head_width=0.6,head_length=0.3)
                        a.arrow(x2,y2+1,0,-1,head_width=0.6,head_length=0.3)
                else:
                    dirx = (x2-x1)/abs(x2-x1)
                    diry=(y2-y1)/abs(y2-y1)
                    cory1=diry*(abs(y2-y1)-1)+y1
                    # a.plot([x1, x1],[y1, cory1],'k')
                    # a.plot([x1, x2],[cory1, cory1],'k')
                    # a.plot([x2, x2],[cory1, y2],'k')
                    # ax.arrow(x1, x1, y1, cory1, head_width=0.01, head_length=0.02, fc='k', ec='k')
                    # ax.arrow(x1, x2, cory1, cory1, head_width=0.01, head_length=0.02, fc='k', ec='k')
                    # ax.arrow(x2, x2, cory1, y2, head_width=0.01, head_length=0.02, fc='k', ec='k')
                    a.arrow(x1,y1,0,cory1-y1,head_width=0.6,head_length=0.3)
                    a.arrow(x1,cory1,x2-x1,0,head_width=0.6,head_length=0.3)
                    a.arrow(x2,cory1,0,y2-cory1,head_width=0.6,head_length=0.3)

                startx = int(dict[key][1])
                starty=int(dict[key][2])
        print "END"
        print "The optimal path length is :", length
        if w=='y':
            print "The total effort in this order is:",effort
        canvas = FigureCanvasTkAgg(f, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", expand=1)
    go_button = tk.Button(root, text='Quit!', width=3,
              height=1, command=root.destroy)
    go_button.pack(side="top")
    root.mainloop()
