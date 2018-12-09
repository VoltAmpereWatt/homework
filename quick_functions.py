import numpy as np

BLOCKLEN = 256
def update_theta(x,updown):
    if updown == 3:
        if x < 0:
            x = 0
    if updown == 1:
        if x > 2**15:
            x = 2**15
    return np.linspace(x,x,BLOCKLEN)

def update_gain(x, updown):
    if updown == 2:
        gain_step = 500
        if x > 2**15:
            x = 1000
        return int(x+gain_step)
    elif updown == 4:
        gain_step = -500
        if x < 1000:
            x = 1000
        return int(x+gain_step)

def display_thresh(thr):
    print("! New threshold = "+str(thr))


