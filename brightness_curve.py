import math

def time_brightness_curve(t):
	if t <= 0.25:
		denom = 1 + math.exp(-t * 8)
		out = 1 - (1 / denom)
		return out * 2
	else:
		denom = 1 + math.exp(-2 - (2 * (t - 0.25)))
		out = 1 - (1 / denom)
		return out * 2