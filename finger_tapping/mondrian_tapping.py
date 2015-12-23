from psychopy import visual, event, core, gui
from psychopy.hardware.emulator import launchScan
from numpy.random import shuffle 
import numpy as np
import pandas as pd
from datetime import datetime

# set_colors()
# Colors used during the experiment.s
def set_colors():
    global sc_c # screen color 1
    global f_c # frame color 2
    global sq_c # square color 3
    # 1 = white
    # -0.06 = grey 80
    # -0.37 = grey 120
    # -1 = black
    sc_c = 1
    f_c = -0.06
    sq_c = -0.37
    t_c = -0.06

# set_sizes()
# Sizes used during the experiment
def set_sizes():
    global f_s # frame size (square) (frame surrounding the stimulus) 1
    global sq_s # square size (square where the stimulus is shown) 2
    global l_s # line size (the width of the line surrounding the stimulus) 3
    f_s = 240
    sq_s = 200
    l_s = 20

# set_positions()
# Positions used during the experiment
def set_positions():
    global fl_p # Where should the flash be drawn 1
    fl_p = [0, 0]
    
# flash stimulus functions
# flash initialization
def flash_init(win, position=[0,0], square_size=10, columns=10, rows=10): 
    global flash # The flash stimulus (an array of flashing squares)
    red = [1, -1, -1] 
    green = [-1, 1, -1]
    blue = [-1, -1, 1]
    yellow = [1, 0.97, -0.55]
    black = [-1, -1, -1]
    color_set = [red, green, blue, yellow, black]
    cell_number = columns * rows
    by_color = int(np.floor(float(cell_number)/len(color_set))) 
    # fill an array with colors. Each color should appear approximatively the same number of times.
    f_colors = []
    for c in color_set:
        for i in range(by_color):
            f_colors.append(c)
    shuffle(color_set)
    i = cell_number - len(f_colors)
    while i > 0:
        f_colors.append(color_set[i])
        i -= 1
    # randomize color order.
    shuffle(f_colors)
    # fill an array with coordinate for each color square. First square should be at the upper left 
    # and next should follow from left to right and up to down.
    xys = []
    x_left = (1 - columns) * square_size / 2
    y_top = (1 - rows) * square_size / 2
    for l in range(rows):
        for c in range(columns):
            xys.append((x_left + c * square_size, y_top + l * square_size))
    flash = visual.ElementArrayStim(win=win, 
                        fieldPos=position,
                        fieldShape='sqr',
                        nElements=cell_number,
                        sizes=square_size,
                        xys=xys,
                        colors=f_colors,
                        elementTex=None,
                        elementMask=None,
                        name='flash',
                        autoLog=False)

# flas255h stimulus change
def flash_change(): 
    global flash
    shuffle(flash.colors)
    flash.setColors(flash.colors)

# set_timing()
# Time variables used during the experiment
def set_timing():
    global f_t # The duration (in frame) of a flash image presentation 1
    f_t = 5
    
#task settings
tr = .770
alternate_time = 20//tr #number of TRs for each block
n_blocks = 25  #12 on, 12 off
task_duration = n_blocks * alternate_time #in TRs, 6 minute scan sessions with 2 second TR
window_dims = [800,600] 
#window_dims = [1920, 1080]                             
subj = raw_input('type subject id: ')
time = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
# settings for launchScan:
MR_settings = { 
    'TR': tr, # duration (sec) per volume
    'volumes': task_duration, # number of whole-brain 3D volumes / frames
    'sync': 't', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 16, #, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'sound': False # in test mode only, play a tone as a reminder of scanner noise
    }
mode = 'Test' #'Test' or 'Scan' or 'None' to choose at startup
globalClock = core.Clock()

infoDlg = gui.DlgFromDict(MR_settings, title='fMRI parameters', order=['TR','volumes'])
if not infoDlg.OK: core.quit()

#Setup task elements
win = visual.Window(window_dims, allowGUI=False, fullscr= False, 
                                 monitor='testMonitor', units='deg')    
set_colors()
set_sizes()
set_positions()
set_timing()
flash_init(win, fl_p, square_size=1, columns=10, rows=10)

sync_now = False
on = False # true when stim is on
stim_switch = False # true when stim switches on or off
last_change = 0

# summary of run timing, for each key press:
data = {'vol':[], 'event':[], 'onset':[], 'duration':[], 'stim_on':[]}

key_code = MR_settings['sync']

# launch: operator selects Scan or Test (emulate); see API docuwmentation
vol = launchScan(win, MR_settings, mode = mode, globalClock=globalClock)
print('Scan start')
print(u"%3d  %7.3f %s\n" % (vol, 0, unicode(key_code)))
duration = MR_settings['volumes'] * tr
# note: globalClock has been reset to 0.0 by launchScan()
while globalClock.getTime() < duration:
    allKeys = event.getKeys()
    for key in allKeys:
        if key != MR_settings['sync']:
            onset = globalClock.getTime()
            print(u"%3d  %7.3f %s\n" % (vol, onset, unicode(key)))
            data['vol'].append(vol)
            data['event'].append(unicode(key))
            data['onset'].append(onset)
            data['duration'].append(.0001)
            data['stim_on'].append(on)
    if 'escape' in allKeys:
        print('user cancel')
        win.close()
        core.quit()
        break
    # detect sync or infer it should have happened:
    if key_code in allKeys:
        sync_now = key_code # flag
        onset = globalClock.getTime()
    if sync_now:
        vol += 1
        tmp = on
        on = vol%(alternate_time*2)>=alternate_time
        stim_switch = (tmp != on)
        print(u"%3d  %7.3f %s\n" % (vol, onset, key_code))
        data['vol'].append(vol)
        data['event'].append(key_code)
        data['onset'].append(onset)
        data['duration'].append(.0001)
        data['stim_on'].append(on)
        if stim_switch and on:
            print(u"%3d  %7.3f %s\n" % (vol, onset, 'stim_on'))
            data['vol'].append(vol)
            data['event'].append('stim_on')
            data['onset'].append(onset)
            data['duration'].append(alternate_time*tr)
            data['stim_on'].append(on)
        if not on:
            if stim_switch:
                print(u"%3d  %7.3f %s\n" % (vol, onset, 'stim_off'))
                data['vol'].append(vol)
                data['event'].append('stim_off')
                data['onset'].append(onset)
                data['duration'].append(alternate_time*tr)
                data['stim_on'].append(on)
            win.flip()
        sync_now = False
    if on:
        if (globalClock.getTime()-last_change) > .1:
            flash_change()
            last_change = globalClock.getTime()
        flash.draw()
        win.flip()
print(u"End of scan (vol 0..%d = %d of %s). Total duration = %7.3f sec" % (vol - 1, vol, MR_settings['volumes'], globalClock.getTime()))
data = pd.DataFrame(data)
data.to_csv('raw_data/' + subj+'_'+time, sep = '\t', index = False)
win.close()
core.quit()