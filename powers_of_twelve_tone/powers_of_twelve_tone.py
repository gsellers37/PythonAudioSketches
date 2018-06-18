from random import randint
from midiutil.MidiFile import MIDIFile
import numpy as np

MyMIDI = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 12
duration = .5
volume = 100

tone_row = np.arange(12)+1
np.random.shuffle(tone_row)

idir = 1
ilen = 626

pitch_range = 96
speed = 300;

for i in range(ilen):
    i = min(i,ilen-i)
    if i == ilen/2:
        idir = -1
        pitch = pitch+pitch_range
    f = np.vectorize(np.int)
    new_row = f(np.power(tone_row,1+i/speed)%pitch_range)
    for note in new_row:
        MyMIDI.addNote(track,channel,pitch+idir*note,time,duration,volume)
        time += duration

binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
