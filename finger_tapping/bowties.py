# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:05:46 2015

@author: Ian
"""

import numpy as np
from psychopy import visual,core,event
import psychopy.monitors.calibTools as calib

from tools import *

my_colors = {'red1':[1,0,0],
                     'red2':[1,0,0], # Twice as likely to occur!
                     'green':[0,1,0],
                     'blue':[0,0,1],
                     'm1':[1,1,0],
                     'm2':[0,0.6,0.6],
                     'm3':[0,0.6,0],
                     'm4':[0.6,0.6,0],
                     'm5':[0,0,0.6],
                     'm6':[0.6,0.6,1]}

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi

#Read a params object from the params file:
p = Params()
f = start_data_file(p.subject)
p.save(f)

f = save_data(f, 'time', 'event') # Events are either color-switches or button presses
                  
window_dims = [800,600]
win = visual.Window(window_dims, allowGUI=False, fullscr= False, 
                                 monitor='testMonitor', units='deg')  

fixation = visual.PatchStim(win, tex=None, mask = 'circle',color=1*rgb,
                                size=p.fixation_size)

#fixation_surround = visual.PatchStim(win, tex=None, mask='circle',
                                         #color=-1*rgb,
                                         #size=p.fixation_size*1.5)
                                         
central_grey = visual.PatchStim(win, tex=None, mask='circle', 
                                                    color=0*rgb, 
                                                    size=p.fixation_size*3)

vertical = [visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc,
                            visibleWedge=[0,
                                          p.angular_width/2]),
                visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc,
                            visibleWedge=[360-p.angular_width/2,
                                                    360]),                                          
                visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc,
                            visibleWedge=[180-p.angular_width/2,
                                          180+p.angular_width/2])]
                            
for v in vertical: v.setSF = p.sf

horizontal = [visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc,
                            visibleWedge=[90-p.angular_width/2,
                                          90 + p.angular_width/2]),
              visual.RadialStim(win,size=p.size,
                            radialCycles=p.radial_cyc,
                            angularCycles=p.angular_cyc,
                            visibleWedge=[270-p.angular_width/2,
                                          270+p.angular_width/2])]

for h in horizontal: h.setSF = p.sf


message = """ PRESS THE KEY \n WHEN YOU SEE THE RED DOT! """
#Initialize and call in one:
Text(win, text=message, height=1.5)() 

#fixation_surround.draw()
fixation.draw()
win.flip()
#Wait 1 sec, to avoid running off:
core.wait(1)
ttl = 0
#After that, wait for the ttl pulse:
while ttl<1:
    for key in event.getKeys():
        if key:
            ttl = 1

# Initialize to True:
switcheroo = True
r_phase_sign = np.sign(np.random.randn(1))
a_phase_sign = np.sign(np.random.randn(1))
t_arr = []
fix_counter = 0
color_arr = []
key_press = []
color_key = 'white'

for block in xrange(p.n_blocks):
    block_clock = core.Clock()
    t=0
    t_previous = 0
    
    while t<p.block_duration:
        t = block_clock.getTime()
        t_diff = t-t_previous 
        if t + (block * p.block_duration) > (fix_counter * p.color_dur):
            fix_counter += 1
            old_color_key = color_key
            while color_key == old_color_key: 
                color_key = my_colors.keys()[np.random.randint(len(my_colors.keys()))]
            
            this_color = my_colors[color_key]
            fixation.setColor(this_color)
            color_arr.append(color_key)
            f = save_data(f, t + (block * p.block_duration), color_key)

        if np.mod(block,2)==0:
            this = vertical
        else:
            this = horizontal
            
        if t>2 and np.mod(int(t),2)==0:
            if switcheroo:
                r_phase_sign = np.sign(np.random.randn(1))
                a_phase_sign = np.sign(np.random.randn(1))
                switcheroo = False

        if np.mod(int(t)-1,2)==0:
            switcheroo = True
            
        # The contrast just reverses (no randomness)
        for thisone in this: thisone.setContrast(np.sin(t*p.temporal_freq*np.pi*2))

        # Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break

        for thisone in this:
            thisone.setRadialPhase(thisone.radialPhase +
                             r_phase_sign*t_diff*two_pi/p.temporal_freq/2)
            
            if block_clock.getTime()>=p.block_duration:
                break
            thisone.setAngularPhase(thisone.angularPhase  +
                               a_phase_sign*t_diff*two_pi/p.temporal_freq/2)
            
            thisone.draw()
            
        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        central_grey.draw()
            
        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        #fixation_surround.draw()

        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
        fixation.draw()
        
        #Keep checking for time:
        if block_clock.getTime()>=p.block_duration:
            break
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