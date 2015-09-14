# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:05:46 2015

@author: Ian
"""

import numpy as np
from psychopy import visual,core,event
import psychopy.monitors.calibTools as calib

from tools import *

rgb = np.array([1.,1.,1.])

#Read a params object from the params file:
p = Params()
f = start_data_file(p.subject)
p.save(f)

f = save_data(f, 'time', 'event') # Events are either color-switches or button presses
                  
window_dims = [800,600]
win = visual.Window(window_dims, allowGUI=False, fullscr= False, 
                                 monitor='testMonitor', units='deg')  

fixation = visual.PatchStim(win, tex=None, mask = 'circle',color=[0, 1, 1],
                                size=p.fixation_size)
                                         
central_grey = visual.PatchStim(win, tex=None, mask='circle', 
                                                    color=0*rgb, 
                                                    size=p.fixation_size*3)

message = """ PRESS THE KEY \n WHEN YOU SEE THE RED DOT! """
#Initialize and call in one:
Text(win, text=message, height=1.5)() 
#Wait 1 sec, to avoid running off:
core.wait(1)
ttl = 0
#After that, wait for the ttl pulse:
while ttl<1:
    for key in event.getKeys():
        if key in ['t', '5']:
            ttl = 1

fix_counter = 0
key_press = []

for block in xrange(p.n_blocks):
    block_clock = core.Clock()
    t=0
    t_previous = 0
    
    while t<p.block_duration:
        t = block_clock.getTime()
        t_diff = t-t_previous 
        if t%10<1:
            fixation.draw()
            win.flip()
        elif t%5<1:
            win.flip()
            

        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break

        #handle key presses each frame
        for key in event.getKeys():
            if key in ['escape','q']:
                win.close()
                f.close()
                core.quit()
            else:
                    key_press.append(t + (block * p.block_duration))
                    f = save_data(f, t + (block * p.block_duration), 'key pressed')


        t_previous = t
        t_arr.append(block_clock.getTime())

win.close()
f.close()
core.quit()