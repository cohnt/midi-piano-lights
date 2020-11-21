import pygame.midi
import board
import neopixel

n_pixels = 177
n_keys = 88
min_key = 21
max_key = 108
color = (255, 0, 0)
important_statuses = {
	"time_update": 248,
	"pedal": 176,
	"note": 144
}

key_status = [False for _ in range(n_keys)]
keypress_times = [0 for _ in range(n_keys)]
brightness = [0 for _ in range(n_keys)]

pixels = neopixel.NeoPixel(board.D18, n_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)

def key_idx_to_strip_leds(idx):
	# Map to [0, 1)
	low = float(idx) / n_keys
	high = float(idx+1) / n_keys
	# Map to [0, n_pixels)
	low = low * n_pixels
	high = high * n_pixels
	return range(low, high)

def note_to_key_idx(note_number):
	# Midi input is in range [min_key, max_key]
	return note_number - min_key

def number_to_note(number):
	# Only needed for debugging
	notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
	return notes[number%12]

pygame.midi.init()
input_device = pygame.midi.Input(3)

try:
	while True:
		# Get new MIDI input if any is available
		if input_device.poll():
			event = input_device.read(1)[0]

			data = event[0]
			timestamp = event[1]

			status = data[0]
			note_number = data[1]
			velocity = data[2]

			if status == important_statuses["time_update"]:
				# We can ignore time updates
				continue
			elif status == important_statuses["pedal"]:
				down = velocity > 0
				print("T=%d\tPedal %s" % (timestamp, "Down" if down else "Up"))
			elif status == important_statuses["note"]:
				down = velocity > 0
				print("T=%d\tNote=%d %s\tVel=%d" % (timestamp, note_number, "Down" if down else "Up", velocity))
except KeyboardInterrupt:
	print("Exiting...")