import mido
from mido import Message, MidiFile, MidiTrack
from random import randint


# "Velocity" is a number between 0 and 127 describes the volume (gain) of a MIDI note 
# Note is a number between 0 and 127. 60 is C4. Add 12 to move up one octave
# Channel is a number between 0 and 15. Channel 10 is reserved for percussion sounds. Different Channels for different instruments
# If the velocity is set to zero. The NOTE ONmessage then has the same meaning as a NOTE OFF message, switching the note off.

def generate_note():
	note_value = randint(60, 72)
	msg = Message('note_on', note=note_value, velocity=80, time=0)
	msg.copy(channel=0)
	return msg

def generate_notes(amount):
	notes = []
	for i in range(amount):
		notes.append(generate_note())
	return notes

def create(file_name, notes):
	# Setup
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)

	# Append each note to track
	for i in range(len(notes)):
		track.append(notes[i])

	# Save new song as a MIDI file
	mid.save(file_name)

def play(file_name):
	# Open saved MIDI file
	mid = MidiFile(file_name)

	# Play all tracks and messages in track
	for i, track in enumerate(mid.tracks):
	    print('Track {}: {}'.format(i, track.name))
	    for msg in track:
	        print(msg)

	# Print port names
	# print(mido.get_output_names())
	# print(mido.get_input_names())

	# Set outport and inports
	inport = mido.open_input('IAC Driver testport')
	outport = mido.open_output('IAC Driver testport')

	# with mido.open_input() as inport:
	#     for msg in inport:
	#         print(msg)

	for msg in mid.play():
		outport.send(msg)

def sanitize_file_name(file_name):
	if len(file_name) >= 4:
		last_four = file_name[-4:]
		print(last_four)
		if last_four == ".mid":
			return file_name
		else:
			file_name += ".mid"
			return file_name
	else:
		file_name += ".mid"
		return file_name


def main():
	print("Enter file name to write to:")
	file_name = sanitize_file_name(input())

	print("How many notes would you like to add?")
	amount = int(input())

	notes = generate_notes(amount)
	print(notes)

	create(file_name, notes)
	play(file_name)

	# Stop
	# have all the notes turn off
	print("How many notes are being played?")
	notes_answer = input()

	print("Guess the lowest note:")
	lowest_note = input()

if __name__ == "__main__":
	main()