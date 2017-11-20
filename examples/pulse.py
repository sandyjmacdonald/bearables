#!/usr/bin/env python

import time
from bearables import set_all, show, clear

clear()
show()

while True:
    for i in range(1, 50) + range(50, 0, -1):
        set_all(1.0 / i)
        show()
        time.sleep(0.01)
