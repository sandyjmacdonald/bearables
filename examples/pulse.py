#!/usr/bin/env python

import time
from bearables import set_all, show, clear

clear()
show()

while True:
    for i in list(range(1, 50)) + list(range(50, 0, -1)):
        set_all(1.0 / i)
        show()
        time.sleep(0.01)
