import pygame.midi
import board
import neopixel

n_pixels = 177
n_keys = 88.0
pixels = neopixel.NeoPixel(board.D18, n_pixels, brightness=1.0, auto_write=False, pixel_order=neopixel.GRB)
min_key = 21
max_key = 108

def number_to_light(note_number):
    led_num = int((note_number - min_key) * (float(n_pixels) / float(n_keys)))
    led_num = (int(n_pixels)) - led_num
    if led_num >= n_pixels:
        return n_pixels
    elif led_num < 0:
        return 0
    else:
        return led_num

def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number%12]

def readInput(input_device):
    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if data[0] != 248:
                if velocity == 127:
                    continue
                if velocity > 0:
                    print (note_number, number_to_note(note_number), velocity, "ON")
                    for i in range(number_to_light(note_number+1), number_to_light(note_number)):
                        pixels[i] = (255, 0, 0)
                    pixels.show()
                else:
                    print (note_number, number_to_note(note_number), velocity, "OFF")
                    for i in range(number_to_light(note_number+1), number_to_light(note_number)):
                        pixels[i] = (0, 0, 0)
                    pixels.show()

if __name__ == '__main__':
    pygame.midi.init()
    my_input = pygame.midi.Input(3) #only in my case the id is 2
    readInput(my_input)
