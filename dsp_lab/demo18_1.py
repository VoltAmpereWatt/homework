# Tk_demo_03_slider.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use two sliders to adjust the frequency and gain.

from math import cos, pi 
import pyaudio
import struct
import sys
import numpy as np 
from scipy import signal

if sys.version_info[0] < 3:
	# for Python 2
	import Tkinter as Tk
else:
	# for Python 3
	import tkinter as Tk   	

def fun_quit():
  global PLAY
  print('I quit')
  PLAY = False

Fs = 8000     # rate (samples/second)
gain = 0.2 * 2**15

# Define Tkinter root
top = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
gain = Tk.DoubleVar()

# Initialize Tk variables
f1.set(200)   # f1 : frequency of sinusoid (Hz)
gain.set(0.2 * 2**15)

# Define buttons
S_freq = Tk.Scale(top, label = 'Frequency', variable = f1, from_ = 100, to = 400, tickinterval = 100)
S_gain = Tk.Scale(top, label = 'Gain', variable = gain, from_ = 0, to = 2**15-1)
Bquit = Tk.Button(top, text = 'Quit', command = fun_quit)

# Place buttons
Bquit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_gain.pack(side = Tk.LEFT)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 1, 
  rate = Fs,
  input = False, 
  output = True,
  frames_per_buffer = 128)            
  # specify low frames_per_buffer to reduce latency

BLOCKLEN = 256
output_block = [0 for n in range(0, BLOCKLEN)]
theta = 0
PLAY = True

a1=gain.get()

print('* Start')
while PLAY:
  top.update()
  om1 = 2.0 * pi * f1.get() / Fs
  x=int(gain.get())
  # g=np.linspace(a,x,BLOCKLEN)
  # if a1 == 0:
  #   g = np.linspace(x-BLOCKLEN,x,BLOCKLEN)
  # else:
  #   g = np.linspace(a,x,BLOCKLEN)
  # print(a1," ",x)
  g=np.linspace(a1,x,BLOCKLEN)  
  
  for i in range(0, BLOCKLEN):
    temp = gain.get() * cos(theta) 
    output_block[i] = int(g[i]*cos(theta))
    # output_block[i] = int(gain.get()*cos(theta))
    theta = theta + om1
  a1=gain.get()
  out = np.array(output_block)
  b,a = signal.butter(2,0.6,'lowpass')
  initial = signal.lfilter_zi(b,a)
  out = signal.lfilter(b,a,out,zi = initial)
  
  if theta > pi:
  	theta = theta - 2.0 * pi
  binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
  stream.write(binary_data)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
