from psychopy import visual, event, core, gui
from psychopy.hardware.emulator import launchScan
from psychopy.sound import Sound

#task settings
alternate_time = 8 #number of TRs for each block
n_blocks = 24  #12 on, 12 off
task_duration = n_blocks * alternate_time #in TRs, 6 minute scan sessions with 2 second TR
window_dims = [800,600]                              

# settings for launchScan:
MR_settings = { 
    'TR': 2.000, # duration (sec) per volume
    'volumes': task_duration, # number of whole-brain 3D volumes / frames
    'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    'sound': True, # in test mode only, play a tone as a reminder of scanner noise
    }
mode = 'Test' #'Test' or 'Scan' or 'None' to choose at startup
globalClock = core.Clock()

infoDlg = gui.DlgFromDict(MR_settings, title='fMRI parameters', order=['TR','volumes'])
if not infoDlg.OK: core.quit()

#Setup task elements
win = visual.Window(window_dims, allowGUI=False, fullscr= False, 
                                 monitor='testMonitor', units='deg')    
fixation_cross=visual.TextStim(win, text='+',font='BiauKai',
                                height=2,color=[1,1,1], colorSpace=u'rgb',
                                opacity=1,depth=0.0,
                                alignHoriz='center',wrapWidth=50)
counter = visual.TextStim(win, height=.5, pos=(0,-4), color=win.rgb+0.5)

# summary of run timing, for each key press:
output = u'vol    onset key\n'
for i in range(-1 * MR_settings['skip'], 0):
    output += u'%d prescan skip (no sync)\n' % i

key_code = MR_settings['sync']
output += u"  0    0.000 %s  [Start of scanning run, vol 0]\n" % key_code
sync_now = False

# launch: operator selects Scan or Test (emulate); see API docuwmentation
vol = launchScan(win, MR_settings, mode = mode, globalClock=globalClock)

max_slippage = 0.02 # how long to allow before treating a "slow" sync as missed
    # any slippage is almost certainly due to timing issues with your script or PC, and not MR scanner

duration = MR_settings['volumes'] * MR_settings['TR']
# note: globalClock has been reset to 0.0 by launchScan()
while globalClock.getTime() < duration:
    allKeys = event.getKeys()
    for key in allKeys:
        if key != MR_settings['sync']:
            output += u"%3d  %7.3f %s\n" % (vol-1, globalClock.getTime(), unicode(key))
    if 'escape' in allKeys:
        output += u'user cancel, '
        win.close()
        core.quit()
        break
    # detect sync or infer it should have happened:
    if MR_settings['sync'] in allKeys:
        sync_now = key_code # flag
        onset = globalClock.getTime()
    if sync_now:
        # do your experiment code at this point; for demo, just shows a counter & time
        counter.setText(u"Elapsed volumes: %d\n%.3f seconds" % (vol, onset))
        output += u"%3d  %7.3f %s\n" % (vol, onset, sync_now)
        counter.draw()
        #alternate fixation
        on = vol%(alternate_time*2)>alternate_time
        if on:
            fixation_cross.draw()
        win.flip()
        vol += 1
        sync_now = False

output += u"End of scan (vol 0..%d = %d of %s). Total duration = %7.3f sec" % (vol - 1, vol, MR_settings['volumes'], globalClock.getTime())
print output
win.close()
core.quit()
