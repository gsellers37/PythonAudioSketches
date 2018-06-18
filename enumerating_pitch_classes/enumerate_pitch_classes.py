from random import randint
from midiutil.MidiFile import MIDIFile

def enumerate_interval_vector(base,vector):
	def helper(chord,vector):
		chords = []
		if vector == [0,0,0,0,0,0]:
			return [chord]
		else:
			for idx,num in enumerate(vector):
				if num>0:
					choices = [idx+1,12-(idx+1)]
					for choice in choices:
						new_chord = chord[:]
						new_vector = vector[:]
						new_note = (new_chord[-1]+choice)%12
						count = 0
						for note in new_chord[:]:
							new_idx = min(abs(new_note - note),12-abs(new_note - note))

							if new_vector[new_idx-1]>0:
								count +=1
								new_vector[new_idx-1]-=1

							else:
								break
						# else:
						# 	print 'breaking choice'
						# 	break
						if count == len(new_chord):
							new_chord.append(new_note)
							chords.extend(helper(new_chord,new_vector))




			return chords

	return helper([base],vector)


# Forward backwards 3rd level intervallic function
interval_classes = [
[2,1,0,0,0,0],
[1,1,1,0,0,0],
[1,0,1,1,0,0],
[1,0,0,1,1,0],
[1,0,0,0,1,1],
[0,2,0,1,0,0],
[0,1,1,0,1,0],
[0,1,0,1,0,1],
[0,1,0,0,2,0],
[0,0,2,0,0,1],
[0,0,1,1,1,0],
]
x = interval_classes.copy()
interval_classes.reverse()
interval_classes.extend(x)

interval_classes = [[4,2,0,2,4,3]]
#
interval_classes = [[9,8,8,8,8,4]]

MyMIDI = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 60
duration = .5
volume = 100
MyMIDI.addNote(track,channel,pitch,time,float(duration),volume)
for interval_class in interval_classes:
	for chord in enumerate_interval_vector(0,interval_class):
	# 	print time
	# 	ontime = []
	# 	breaktime = []
	# 	divisions = 3
	# 	for i in range(len(chord)):
	# 		ontime.append(randint(1,divisions))

	# 	full_time = sum(ontime)
	# 	for i in range(len(chord)):
	# 		if i == 0:
	# 			breaktime.append(randint(0,len(chord)*divisions-full_time))
	# 		elif i == len(chord)-1:
	# 			breaktime.append(len(chord)*divisions-full_time-sum(breaktime))
	# 		else:
	# 			breaktime.append(len(chord)*divisions-full_time-sum(breaktime))
	# 	for i in range(len(breaktime)):

	# 		breaktime[i] = duration*breaktime[i]/(divisions)



		# for idx,note in enumerate(chord):
		# 	MyMIDI.addNote(track,channel,pitch+note,time,duration*ontime[idx]/divisions,volume)

		# 	time += duration*ontime[idx]/divisions
		# 	time += breaktime[idx]

		for note in chord:
			MyMIDI.addNote(track,channel,pitch+note,time,duration,volume)
		pitch = 60+ chord[2]
		time += duration
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
