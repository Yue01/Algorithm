import Tkinter as tk
import ttk
from Tkinter import *

def print_selection():
    l.config(text='you have selected ' + var.get())
    print str(var.get())


win = tk.Tk()
var = tk.StringVar()
win.title('EECS221A App')
win.geometry('800x400')

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

f=tk.Label(left, width=20, text='6.Which file to process?',bg='white')
f.pack(side="top")
file= Frame(left)
file.pack(side = "top")
# right_sentence=tk.Label(right, width=20, text='The result is shown here:')
# right_sentence.pack(side="top")
end= Frame(right)
end.pack(side = "top")

bottomframe = Frame(left)
bottomframe.pack( side = "bottom" )


# first title
l = tk.Label(algorithm,width=20, text='1.Algorithm',bg='white')
l.pack(side="top")
# selection
r1 = tk.Radiobutton(al_select,text='Nearest Neighbor',
                    variable=var, bg='white',value='n',
                    command=print_selection)
r1.pack(side="top")
r2 = tk.Radiobutton(al_select,text='Branch and Bound',
                    variable=var, bg='white',value='b',
                    command=print_selection)
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
                    variable=var, bg='white',value='y',
                    command=print_selection)
w_1.pack(side="left")
w_2 = tk.Radiobutton(weight,text='No',
                    variable=var,bg='white',value='n',
                    command=print_selection)
w_2.pack(side="left")
# input max weight:
l = tk.Label(w_select,width=5, text='max:',bg='white')
l.pack(side="left")

w=tk.Entry(w_select,width=5)
w.pack(side="left")
dw = tk.Label(w_select,width=5, text='(kg)',bg='white')
dw.pack(side="left")

# list of files:
number = tk.StringVar()
numberChosen = ttk.Combobox(file, width=22, textvariable=number)
numberChosen['values'] = ("warehouse-orders-1item.csv", "warehouse-orders-3item.csv", "warehouse-orders-5item.csv", "warehouse-orders-10item.csv", "warehouse-orders-21item.csv")
numberChosen.pack(side = "top")
numberChosen.current(0)

# at the end:
b = tk.Button(bottomframe, text='Start!', width=5,
              height=1)#, command=hit_me)
b.grid(row=3,column=1)
win.mainloop()
