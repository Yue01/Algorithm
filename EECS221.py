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
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from draw import draw_graph
from draw import draw_reset



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
canvas_list=[]
all_order_list=[]
res_list=[]
current_total_weight=0
queue = Q.PriorityQueue()

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
    qwerlist=[]
    with open('result.txt', 'r') as file:
        read = file.readline()
        qwerlist = list(read)
        for i in range(0,len(qwerlist)):
            print qwerlist[i]


def reset_para():
    global current_total_weight
    global queue
    global canvas_list
    current_total_weight=0
    queue=Q.PriorityQueue()
    canvas_list=[]
    BNB_reset()
    draw_reset()
#the start button activity in GUI
def hit_me():
    global canvas_list
    global order_name
    global start_point
    global end_point
    global current_total_weight
    current_total_weight=0
    canvas_list=[]
    start_point[0]=int(s_x.get())
    start_point[1]=int(s_y.get())
    end_point[0]=int(e_x.get())
    end_point[1]=int(e_y.get())
    #order_name=str(numberChosen.get())
    with open('warehouse-orders-v02-tabbed.txt', 'r') as file:
        read = file.readline()
        while not (read==""):
            if not read:
                break
            order = read.split()
            all_order_list.append(order)
            # then with the optimal path
            res_dict=singleorder(order)
            res_list.append(res_dict)
            read = file.readline()
    file.close()
    num_of_res.set(len(all_order_list))
    # canvas = FigureCanvasTkAgg(fig, master=right)
    # canvas.draw()
    # canvas.get_tk_widget().pack(side="right", expand=1)
def add_order():
    global current_total_weight
    global canvas_list
    global w
    global all_order_list
    x=0
    y=0
    #输入的order 号
    num_order=int(choose_input.get())
    #最大的weight
    no_w = int(w_qwer.get())
    cur_order = all_order_list[num_order-1]
    for i in range(0,len(cur_order)):
        cur_id = cur_order[i]
    # To professor:
    # Here I am confused that almost all the itemid in "weight" and "item" don't match
    # for example, I looked up all the ids in the first 20 order, only 2 of the items show up in "weight" file
    # as a result, almost all the nodes show: "weight missing" (when the weight is a factor),which I don't think makes sense
    # So to prove that my algorithm really works: give them the default value,and use this for batch processing
        if(w=="y"):
            #weight= dict_w[cur_id]
            weight=2
        else:
            weight=2
        pos=dict[cur_id]
        x=int(pos[0])
        y=int(pos[1])
        cur_info = [weight,x,y,cur_id]
        new_item = Item(cur_info)
        queue.put(new_item)
        current_total_weight+=weight
    if(w=="y" and current_total_weight>=no_w):
        fd.set("It's full!")
    else:
        fd.set("Not full yet!")





    #review = str(receive(canvas_list[num_order-1],no_w,w))
    #fd.set(review)

def process():
    global canvas_list
    #最大的weight
    sum=0
    no_w = int(w_qwer.get())
    new_order=[]
    new_res={}
    if(w=="n"):
        while not queue.empty():
            first_item = queue.get()
            new_order.append(first_item.list[3])
        # optimal path
        canvas_dict=singleorder(new_order)
        canvas_list.append(canvas_dict)
    else:
        while not queue.empty():
            first_item = queue.get()
            print "The current stuff：：：：：：：：：：：：：：：：：：：：：：：：：：：："
            print first_item.list
            if(sum+int(first_item.list[0])>=no_w):
                canvas_dict=singleorder(new_order)
                canvas_list.append(canvas_dict)
                new_order=[]
                new_order.append(first_item.list[3])
                sum=first_item.list[0]
            else:
                new_order.append(first_item.list[3])
                sum+=first_item.list[0]
        if not len(new_order)==0:
            canvas_dict=singleorder(new_order)
            canvas_list.append(canvas_dict)

    print "current split is :"
    print canvas_list
    # f = open('result.txt','w')
    # f.write(str(canvas_list))
    # f.close()
    draw_graph(canvas_list)




    # sl = []
    # sl.append(0)
    # start_point[0]=int(s_x.get())
    # start_point[1]=int(s_y.get())
    # sl.append(start_point[0])
    # sl.append(start_point[1])
    # el=[]
    # el.append(0)
    # end_point[0]=int(e_x.get())
    # end_point[1]=int(e_y.get())
    # el.append(end_point[0])
    # el.append(end_point[1])
    # review = str(original_start(sl,el))
    # fd.set(review)



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

# # initialize: start, end, order and time
# start_point=input("Hello User, where is your worker? [x,y] : ")
# #start_point=start_point_arb.split()
# end_point=input("What is your worker's end location? [x,y] : ")
# #end_point=end_point_ard.split()
# max_time = int(raw_input('Enter the amount of seconds you want to run this: '))

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
    # improvement for nearest neighbour: select different start

    #put all nodes in this dictionary
    for i in range(0,len(order)):
        place = dict[order[i]]
        # dict5 用来存放order number
        dict5[i]=order[i]
        dict1[i]=place
    dict2=dict1.copy()





    # use mst to generate the lower bound
    #generatemst(dict2,start_point,end_point)
    # using Branch and Bound algorithm
    if(choice=="b"):
        return branch(dict2,dict_w,start_point,end_point,w,dict5)
    # improvement for nearest neighbour
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) <0.01:
        opt=0
        curd=0
        pathlist=[]
        dict3={}
        dict3=copy.deepcopy(dict1)

        # choose a point to start and remove it
        key2 = random.choice(dict3.keys())
        startx = start_point[0]
        starty = start_point[1]
        endx=end_point[0]
        endy=end_point[1]
        tem = dict3[key2]
        curx = tem[0]
        cury = tem[1]
        temp_dir = direction
        curd = get_dis(startx,starty,curx,cury)
        direction=temp_dir
        #curd = abs(startx-curx)+abs(starty-cury)
        opt= opt+curd
        startx=curx
        starty=cury
        pathlist.append(key2)
        dict3.pop(key2)

        while(len(dict3)>0):
            distance =sys.maxint
            for key in dict3:
                tem = dict3[key]
                curx = tem[0]
                cury = tem[1]
                curd = abs(startx-curx)+abs(starty-cury)
                if(curd<=distance):
                    distance=curd
                    next=key
            pathlist.append(next)
            node = dict3[next]
            startx=node[0]
            starty=node[1]
            dict3.pop(next)

        # generate tree grapgh for NN

        startx=start_point[0]
        starty=start_point[1]
        for i in range(len(pathlist)):
            col = dict1[pathlist[i]]
            opt=opt+abs(col[0]-startx)+abs(col[1]-starty)
            startx=col[0]
            starty=col[1]
        endx=end_point[0]
        endy=end_point[1]
        opt=opt+abs(endx-startx)+abs(endy-starty)
        if(opt<opt_final):
            pathlist_final=pathlist
            opt_final=opt


    pathlist=pathlist_final
    # generate tree for NN
    dict4=copy.deepcopy(dict1)
    lv=0
    new=""
    now=""
    select=0
    g = gv.Digraph(format='pdf')
    last="lv "+str(lv)+",node (" + str(start_point[0])+","+str(start_point[1])+")"
    for i in range(0,len(pathlist)):
        lv+=1
        for key in dict4:
            now = "lv "+str(lv)+",node (" + str(dict4[key][0])+","+str(dict4[key][1])+")"
            g.edge(str(last),str(now))
            if(key==pathlist[i]):
                new=now
                select=key
        dict4.pop(select)
        last=new

    now="lv "+str(lv+1)+",node (" + str(end_point[0])+","+str(end_point[1])+")"
    g.edge(str(last),str(now))
    #g.render('test-output/Nearest_Neighbor.gv', view=True)
    # now print the path
    opt=0
    print("6. Here is the optimal picking order:")
    print pathlist
    print("7. Here is the optimal path:")
    if(w=="n"):
        opt=0
        direction =1
        temp_dict={}
        info=[]
        print "Nearest Neighbor:"
        print "If weight not in factor, the path will be:"
        print("("),
        print(start_point[0]*2),
        startx=start_point[0]*2
        print(","),
        print(start_point[1]*2),
        starty=start_point[1]*2
        info.append(0)
        info.append(startx)
        info.append(starty)
        temp_dict[0]=info
        print(")->"),
        for i in range(len(pathlist)):
            info=[]
            col = dict2[pathlist[i]]
            opt+=get_dis(startx,starty,col[0]*2,col[1]*2)
            #opt=opt+abs(col[0]*2-startx)+abs(col[1]*2-starty)
            startx=col[0]*2
            starty=col[1]*2
            info.append(0)
            info.append(startx+direction)
            info.append(starty)
            temp_dict[i+1]=info
            print("("),
            print(col[0]*2),
            print(","),
            print(col[1]*2),
            print(")->"),
        endx=end_point[0]*2
        endy=end_point[1]*2
        #opt=opt+abs(endx-startx)+abs(endy-starty)
        opt+=get_dis(startx,starty,endx,endy)
        info=[]
        info.append(0)
        info.append(endx+direction)
        info.append(endy)
        temp_dict[len(pathlist)+1]=info
        print("("),
        print(end_point[0]*2),
        print(","),
        print(end_point[1]*2),
        print(")->"),
        print("END")
        print("8. The optimal path length is : "),
        print opt
        print "info~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print temp_dict
        print("\n")
        return temp_dict
    else:
        direction=1
        temp_dict={}
        info=[]

        list=[]
        total_weight=0
        weight={}
        # 选择之后的path顺序
        list=copy.copy(pathlist)
        #dict5里存有相应序号对应的itemid
        num_dict = copy.deepcopy(dict5)
        #weight有所有物品的重量
        weight=copy.deepcopy(dict_w)
        now_dict = copy.deepcopy(dict2)
        tem_list = []
        tem_list.append(0)
        s=''
        s1=0
        select=""
        for i in range(1,len(list)-1):
            col = dict2[list[i]]
            for key in now_dict:
                if(now_dict[key][0]==col[0] and now_dict[key][1]==col[1]):
                    select=key
                    s=num_dict[key]
                    s1=int(s)
                    tem_list.append(s1)
            now_dict.pop(select)
            num_dict.pop(select)
        print "thins are here"
        print dict2
        print "Nearest Neighbor:"
        print "If weight in factor, the path will be: "
        x_1=start_point[0]*2
        y_1=start_point[1]*2
        info.append(0)
        info.append(x_1+direction)
        info.append(y_1)
        temp_dict[0]=info
        print"(",x_1+direction,",",y_1,")->",
        now_w=0
        for i in range(1,len(list)):
            info=[]
            col = dict2[list[i]]
            x_2=col[0]*2
            y_2=col[1]*2
            tem_w = 0
            try:
                # tem_w=weight[dict5[tem_list[len(list)-1]]]
                tem_w = random.randint(1, 5)
                total_weight+=tem_w
                print "(weight: ",tem_w,")",
            except KeyError:
                tem_w=0
                total_weight+=tem_w
                print "(weight missing! )",
            info.append(tem_w)
            wdis = get_dis(x_1,y_1,x_2,y_2)
            info.append(x_2+direction)
            info.append(y_2)
            temp_dict[i]=info
            print"(",x_2+direction,",",y_2,")->",
            now_w += wdis*total_weight
            x_1=x_2
            y_1=y_2
        x_2=end_point[0]*2
        y_2=end_point[1]*2
        info=[]
        info.append(0)
        info.append(x_2)
        info.append(y_2)
        temp_dict[len(list)]=info
        try:
            # To professor:
            # Here I am confused that almost all the itemid in "weight" and "item" don't match, and I don't know why
            # for example, I looked up all the ids in 5-item order, none of them shows up in item csv
            # as a result, almost all the nodes show: weight missing
            # to prove that my algorithm works: give them random value from 1-5,and use this for batch processing
            # such is the same with bnb. Please inform me if I'm wrong or how to fix this! Thanks!
            # to find the weight from the file:
            # tem_w=weight[dict5[tem_list[len(list)-1]]]
            tem_w = random.randint(1, 5)
            total_weight+=tem_w
            print "(weight: ",tem_w," )",
        except KeyError:
            tem_w=0
            print "(weight missing! )",
        print"(",x_2,",",y_2,")->",

    print "END"
    print "The total effort is :", now_w
    print
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
            # use the mst to generate a lower bound
            #generatemst(order, start_point,end_point)
    f.close()
# input the time limit

# arbitrary input
# order_name=raw_input("Please list file of orders to be processed:")
# allorder(order_name)

win = tk.Tk()
var1= tk.StringVar()
var2 = tk.StringVar()
win.title('EECS221A App')
win.geometry('170x500')


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
# right_sentence=tk.Label(right, width=20, text='The result is shown here:')
# right_sentence.pack(side="top")
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

# list of files:
# number = tk.StringVar()
# numberChosen = ttk.Combobox(file, width=22, textvariable=number)
# numberChosen['values'] = ("warehouse-orders-1item.csv", "warehouse-orders-3item.csv", "warehouse-orders-5item.csv", "warehouse-orders-10item.csv", "warehouse-orders-21item.csv")
# numberChosen.pack(side = "top")
# numberChosen.current(0)

#draw something
# fig = Figure(figsize=(3, 3.5), dpi=100)
# a = fig.add_subplot(111)
# a.set_axis_off()
# plt.xlim(-1,21)
# plt.ylim(-1,21)
# for i in range(1,11):
#     for j in range(1,11):
#         a.plot(2*i,2*j,'go')

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

draw = tk.Button(choose, text='Add', width=4,
              height=1, command=add_order)
draw.pack(side="left")
go_button = tk.Button(choose, text='Go!', width=3,
              height=1, command=process)
go_button.pack(side="left")
latest = tk.Button(other_op, text='Latest', width=5,
              height=1, command=read_latest)
latest.pack(side="top")
reset = tk.Button(other_op, text='Reset', width=5,
              height=1, command=reset_para)
reset.pack(side="top")


# qwer = tk.Button(bottomframe, text='lol', width=5,
#               height=1, command=right.restart)
# qwer.grid(row=4,column=1)
win.mainloop()







#g=np.array([[start_point[0],start_point[1]]])
#for i in range(1,len(order)):
#    item = dict[order[i]]
#    g = np.concatenate((g,[item]))
#g = np.concatenate((g,[[end_point[0],end_point[1]]]))
#size = len(g)

# Create a list to represent the original order considering the start point
# print path
# functions
# calculating the distance
