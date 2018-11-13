import sys
import math
if sys.version_info[0] < 3:
	# for Python 2
	import Tkinter as Tk
else:
	# for Python 3
	import tkinter as Tk

def StringCheck():
    # x = E1.get(self)
    if E1.get().isnumeric():
        L2.configure(text = 'Entered value is a number')
    else:
        L2.configure(text = 'Entered value is a string')

def SliderConfig(event):
    if state.get() == 1:
        L3.configure(text = 'The current value of the slider is: ' + "{:.2f}".format(math.log(0.00001+S1.get())))
    else:
        L3.configure(text = 'The current value of the slider is: ' + str(S1.get()))

def closer(event):
    if event.char == 'q':
        top.quit()

top = Tk.Tk()

# Define Tk variables
# x = Tk.DoubleVar()              # floating point value
# s.set(str(x.get()))
top.bind("<Key>", closer)
state = Tk.IntVar()
L1 = Tk.Label(top, text = "Enter some text")
E1 = Tk.Entry(top)
B1 = Tk.Button(top, text = 'Check', command = StringCheck)
L2 = Tk.Label(top)
S1 = Tk.Scale(top, command = SliderConfig, orient = 'horizontal')
L3 = Tk.Label(top)
C1 = Tk.Checkbutton(top, text = "Logarithmic Slider", variable = state, onvalue = 1, offvalue = 0)

L1.pack()
E1.pack()
B1.pack()
L2.pack()
C1.pack()
S1.pack()
L3.pack()
top.mainloop()