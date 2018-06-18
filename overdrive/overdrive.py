import os
import sys
sys.path.append('..\..')
from Ocelot import *

num_channels = 2
buffer_size = 1024
sample_rate = 44100
sample_width = 2
filename = os.path.basename(__file__).split('.')[0]

writer = AudioWriter(num_channels, sample_rate, sample_width, filename)
audio = AudioController(num_channels,sample_rate, buffer_size,listener=writer)
master = Mixer()
audio.set_generator(master)

#Overdrive1
# settings = [5,10,30,.004,10]


#Overdrive2
# settings = [5, 100, 30, 0.005, 10]


#Overdrive3
settings = [5,10,100,.005,1]

num = settings[0]
divisor = settings[1]
freq = settings[2]
length = settings[3]
gain = settings[4]

for i in range(num):
	master.add(SineGen(freq*((i+divisor)/divisor))*gain*SineGen(length)*SineGen(length))

# audio.render(1/length/2,sample_rate)

while(True):
	audio.update()
