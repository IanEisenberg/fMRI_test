# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:05:46 2015

@author: Ian
"""

import numpy as np
from psychopy import visual,core,event, gui
from psychopy.hardware.emulator import launchScan
from tools import *


# settings for launchScan:
MR_settings = { 
    'TR': 2.000, # duration (sec) per volume
    'volumes': 5, # number of whole-brain 3D volumes / frames
    'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'sound': True # in test mode only, play a tone as a reminder of scanner noise
    }
infoDlg = gui.DlgFromDict(MR_settings, title='fMRI parameters', order=['TR','volumes'])

    
rgb = np.array([1.,1.,1.])

#Read a params object from the params file:
p = Params()
f = start_data_file(p.subject)
p.save(f)

f = save_data(f, 'time', 'event') # Events are either color-switches or button presses
                  
window_dims = [800,600]
win = visual.Window(window_dims, allowGUI=False, fullscr= p.full_screen, 
                                 monitor='testMonitor', units='deg')                                  
fixation_cross=visual.TextStim(win, text='+',font='BiauKai',
                                height=p.fixation_size,color=[1,1,1], colorSpace=u'rgb',
                                opacity=1,depth=0.0,
                                alignHoriz='center',wrapWidth=50)
                            


message = """Waiting for the scanner..."""
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
timer = core.CountdownTimer(0)
t_arr = []
on = False

for block in xrange(p.n_blocks):
    timer.add(p.block_duration)
    while timer.getTime()>0:
        t = p.block_duration-timer.getTime()
        if block%2 == 0:
            fixation_cross.draw()
            win.flip()
        else:
            win.flip()
            

        #Keep checking for time:
        if timer.getTime()<0:
            break

        #handle key presses each frame
        for key in event.getKeys():
            print(key)
            if key in ['escape','q']:
                win.close()
                f.close()
                core.quit()
            else:
                t_elapsed = p.block_duration-t
                key_press.append((key, t_elapsed + (block * p.block_duration)))
                f = save_data(f, t_elapsed + (block * p.block_duration), 'key pressed')


        t_arr.append(p.block_duration-t)

win.close()
f.close()
core.quit()