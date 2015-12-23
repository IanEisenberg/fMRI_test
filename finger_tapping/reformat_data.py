# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:55:30 2015

@author: Ian
"""
"""
Data was initially saved badly (no duration, stim didn't have an associated event)
This file transforms the data into the correct format
Original files also had a bug where stim_on and stim_off times weren't the same.
This file does not account for that problem
"""
import pandas as pd
f = pd.read_csv('002_2.0mm_2015-10-07_10.29.40','\t')
f.columns = ['row','event','onset','vol','stim_on']
f=f.drop('row',axis = 1)
f['duration'] = .0001
tmp = f.stim_on
new = pd.DataFrame()
start_i = 0
for i in range(1,len(tmp)):
    curr = tmp[i]
    last = tmp[i-1]
    switch = (curr != last)
    if switch:
        if curr ==1:
            event = 'stim_on'
        else:
            event = 'stim_off'
        pre = f[start_i:i+1]
        start_i = i+1
        new_row = f.iloc[i]
        new_row['event'] = event
        new_row['duration'] = 19.25
        new = pd.concat([new,pre.append(new_row)])
new.to_csv('002_2.0mm_2015-10-07_10.29.40', index = False, sep = '\t')
