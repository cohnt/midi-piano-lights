import pygame.midi
import board
import neopixel
import math
import time
from brightness_curve import time_brightness_curve
from matplotlib import cm

n_pixels = 177
n_keys = 88
min_key = 21
max_key = 108
important_statuses = {
	"time_update": 248,
	"pedal": 176,
	"note": 144
}
colormap_name = "viridis"
colormap = cm.get_cmap(colormap_name).set_clim(0, n_keys-1)
colors = [colormap(i) for i in range(n_keys)]

pedal_mode = True

key_status = [False for _ in range(n_keys)]
keypress_times = [0 for _ in range(n_keys)]
brightness = [0 for _ in range(n_keys)]
pedal_status = False
pedaled_notes = [False for _ in range(n_keys)]

pixels = neopixel.NeoPixel(board.D18, n_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)

def key_idx_to_strip_leds(idx):
	# Map to [0, 1)
	low = float(idx) / n_keys
	high = float(idx+1) / n_keys
	# Flip (because my controller is on the right side)
	temp = low
	low = 1 - high
	high = 1 - temp
	# Map to [0, n_pixels)
	low = int(low * n_pixels)
	high = int(high * n_pixels)
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
			velocity = data[2] # For now, velocity is just used to determine if it was a press or release

			if status == important_statuses["time_update"]:
				# We can ignore time updates
				continue
			elif status == important_statuses["pedal"]:
				down = velocity > 0
				print("T=%d\tPedal %s" % (timestamp, "Down" if down else "Up  "))
				pedal_status = down
				if down:
					for i in range(n_keys):
						if key_status[i]:
							pedaled_notes[i] = True
				else:
					for i in range(n_keys):
						pedaled_notes[i] = False
			elif status == important_statuses["note"]:
				down = velocity > 0
				print("T=%d\tNote=%d (%s) %s\tVel=%d" % (timestamp, note_number, number_to_note(note_number), "Down" if down else "Up  ", velocity))
				# Update note status
				key_idx = note_to_key_idx(note_number)
				if down:
					key_status[key_idx] = True
					keypress_times[key_idx] = time.time()
					if pedal_status:
						pedaled_notes[key_idx] = True
				else:
					key_status[key_idx] = False
		#
		# Update brightness levels
		current_time = time.time()
		for i in range(n_keys):
			if(key_status[i] == False and not pedaled_notes[i]):
				brightness[i] = 0
			else:
				brightness[i] = time_brightness_curve(current_time - keypress_times[i])
		#
		# Update the pixels
		for i in range(n_keys):
			this_key_brightness = brightness[i]
			this_key_color = (
				int(this_key_brightness * colors[i][0]),
				int(this_key_brightness * colors[i][1]),
				int(this_key_brightness * colors[i][2]),
			)
			this_key_pixels = key_idx_to_strip_leds(i)
			for j in this_key_pixels:
				pixels[j] = this_key_color
		pixels.show()
	#
except KeyboardInterrupt:
	print("Exiting...")
	input_device.close()