

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

time = np.array([0])
freq1 = np.array([0])
freq2 = np.array([0])
phrases = [[4,[5,15],[20,750],[.5,1.5]],
		[5,[5,10],[500,1000],[.5,1.5]],
		[5,[5,10],[20,750],[.5,1.5]],
		[3,[10,20],[1000,2000],[.5,1.5]],
		[2,[10,20],[20,100],[.5,1.5]],
		[250,[0,.1],[20,1000],[.5,1.5]],
		[500,[0,.05],[20,3000],[.5,1.5]],
		[500,[0,.05],[20,1000],[.5,1.5]],
		[3,[10,20],[20,100],[.5,1.5]],
	   ]

render_time = 0
for phrase in phrases:
	render_time += phrase[0]*(phrase[1][0]+phrase[1][1])*1/2

def hold_last_point(last_point):
	return last_point

index_scale = 500
num_osc = 5
for _ in range(num_osc):
	time = np.array([])
	freq1 = np.array([])
	freq2 = np.array([])
	for phrase in phrases:

		#unpack phrase into more easily readable variables
		l = phrase[0]
		timespace_scale = phrase[1]
		freqrange_scale = phrase[2]
		modulator_scale = phrase[3]

		#Create time and modulation arrays
		index = index_scale*np.random.rand()
		time  = np.concatenate((time,  np.random.rand(l)*np.diff(timespace_scale) + timespace_scale[0]),axis=0)
		freq1 = np.concatenate((freq1, np.random.rand(l)*np.diff(freqrange_scale) + freqrange_scale[0]),axis=0)
		freq2 = np.concatenate((freq2, np.random.rand(l)*np.diff(freqrange_scale) + freqrange_scale[0]),axis=0)

	time = np.cumsum(time)
	basefreq = Envelope(np.stack((time,freq1),axis=1),find_next_point = hold_last_point)
	modulator = index * SineGen(Envelope(np.stack((time,freq2),axis=1),find_next_point = hold_last_point))
	master.add(SineGen(basefreq+modulator)/num_osc)


# l = 1
# timespace_scale = [1, 10]
# freqrange_scale = [20,500]
# modulator_scale = [.5, 1.5]
# index_scale = 500
# num_osc = 10
# for i in range(num_osc):
# 	index = index_scale*np.random.rand()
# 	time = np.cumsum(np.random.rand(l)*np.diff(timespace_scale)+timespace_scale[0])
# 	time = np.cumsum(time)
# 	freq1 = np.random.rand(l)*np.diff(freqrange_scale) + freqrange_scale[0]
# 	freq2 = np.random.rand(l)*np.diff(freqrange_scale) + freqrange_scale[0]
# 	basefreq = Envelope(np.stack((time,freq1),axis=1))
# 	modulator = index * SineGen(Envelope(np.stack((time,freq2),axis=1)))
# 	master.add(SineGen(basefreq+modulator)/num_osc)


audio.render(render_time,sample_rate)
# while(True):
	# audio.update()
