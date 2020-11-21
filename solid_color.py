import pygame.midi
import board
import neopixel

n_pixels = 177
n_keys = 88.0
min_key = 21
max_key = 108
color = (255, 0, 0)

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
my_input = pygame.midi.Input(3)

try:
	while True:
		# Get new MIDI input if any is available
		if input_device.poll():
			event = input_device.read(1)[0]
			data = event[0]
			timestamp = event[1]
			note_number = data[1]
			velocity = data[2]
			print("%d\t%d\t%d" % (timestamp, note_number, velocity))
except KeyboardInterrupt:
	print("Exiting...")