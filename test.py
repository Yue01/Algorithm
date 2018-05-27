import Tkinter as tk
import ttk
from Tkinter import *




win = tk.Tk()
var = tk.StringVar()
win.title('EECS221A App')
win.geometry('400x500')

w=tk.Label(win, width=20, text='Factor in weight?')
w.grid(row=1,column=1)


r1 = tk.Radiobutton(win,text='Nearest Neighbor',
                    variable=var, value='n'
                    )
r1.grid(row=2,column=1)
r2 = tk.Radiobutton(win,text='Branch and Bound',
                    variable=var, value='b')
r2.grid(row=3,column=1)
ws=tk.Label(win, width=20, text='If yes, input max weight:')
ws.grid(row=4,column=1)




win.mainloop()
