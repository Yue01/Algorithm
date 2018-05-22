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
from MST import generatemst
from MST import check

#original path length
origin=0
opt=0

# use a dictionary to save all the nodes
dict={}  # for all the items
dict_w={} # for weight information
orderdict={} # for all the orders

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

# initialize: start, end, order and time
start_point=input("Hello User, where is your worker? [x,y] : ")
#start_point=start_point_arb.split()
end_point=input("What is your worker's end location? [x,y] : ")
#end_point=end_point_ard.split()
max_time = int(raw_input('Enter the amount of seconds you want to run this: '))

'''
start_time = time.time()  # remember when we started
while (time.time() - start_time) < max_time:
    do_stuff()
'''

# functions


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




    choice = raw_input("Choose an algorithm:(n for nearest neighbor/b for B&B)")
    w = raw_input("Factor in weight? (y/n):")
    # use mst to generate the lower bound
    #generatemst(dict2,start_point,end_point)
    # using Branch and Bound algorithm
    if(choice=="b"):
        branch(dict2,dict_w,start_point,end_point,w,dict5)
        return

    # improvement for nearest neighbour
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
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
        curd = abs(startx-curx)+abs(starty-cury)
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
        print "Nearest Neighbor:"
        print "If weight not in factor, the path will be:"
        print("("),
        print(start_point[0]*2),
        startx=start_point[0]*2
        print(","),
        print(start_point[1]*2),
        starty=start_point[1]*2
        print(")->"),
        for i in range(len(pathlist)):
            col = dict2[pathlist[i]]
            opt=opt+abs(col[0]*2-startx)+abs(col[1]*2-starty)
            startx=col[0]*2
            starty=col[1]*2
            print("("),
            print(col[0]*2),
            print(","),
            print(col[1]*2),
            print(")->"),
        endx=end_point[0]*2
        endy=end_point[1]*2
        opt=opt+abs(endx-startx)+abs(endy-starty)
        print("("),
        print(end_point[0]*2),
        print(","),
        print(end_point[1]*2),
        print(")->"),
        print("END")
        print("8. The optimal path length is : "),
        print opt
        print("\n")
        return
    else:
        list=[]
        total_weight=0
        weight={}
        # 选择之后的path顺序
        list=copy.copy(pathlist)
        #dict5里存有相应序号对应的itemid
        num_dict = dict5.copy()
        #weight有所有物品的重量
        weight=dict_w.copy()
        now_dict = dict2.copy()
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
        print"(",x_1,",",y_1,")->",
        now_w=0
        for i in range(1,len(list)):
            col = dict2[list[i]]
            x_2=col[0]*2
            y_2=col[1]*2
            tem_w = 0
            try:
                tem_w=weight[dict5[tem_list[i-1]]]
                total_weight+=tem_w
                print "(weight: ",tem_w,")",
            except KeyError:
                tem_w=0
                total_weight+=tem_w
                print "(weight missing! )",
            print"(",x_2,",",y_2,")->",
            now_w += (abs(x_1-x_2)+abs(y_1-y_2))*total_weight
            x_1=x_2
            y_1=y_2
        x_2=end_point[0]*2
        y_2=end_point[1]*2
        try:
            tem_w=weight[dict5[tem_list[len(list)-1]]]
            total_weight+=tem_w
            print "(weight: ",tem_w," )",
        except KeyError:
            tem_w=0
            print "(weight missing! )",
        print"(",x_2,",",y_2,")->",

    print "END"
    print "The total effort is :", now_w
    print
    print

















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
order_name=raw_input("Please list file of orders to be processed:")
allorder(order_name)





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
