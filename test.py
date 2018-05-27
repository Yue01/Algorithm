import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
plt.xlim(-1,21)
plt.ylim(-1,21)
for i in range(1,11):
    for j in range(1,11):
        a.plot(2*i,2*j,'go')


# a tk.DrawingArea
def onclick():
    print "sdfsdfsd"
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)






# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='wtf', command=onclick())
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
