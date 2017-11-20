#!/usr/bin/env python

import time
import random
from bearables import set_led, show, clear

clear()
show()

while True:
    clear()
    leds = random.sample(range(12), random.randint(2, 6))
    for led in leds:
        set_led(led, 1.0)
    show()
    time.sleep(0.1)
