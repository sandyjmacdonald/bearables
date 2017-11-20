#!/usr/bin/env python

import time
from bearables import set_led, show, clear

leds = [1.0, 0.75, 0.25] + [0.0] * 9

clear()
show()

while True:
    for i in range(12):
        set_led(i, leds[i])
    show()
    leds = leds[1:] + [leds[0]]
    time.sleep(0.05)
