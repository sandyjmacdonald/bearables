#!/usr/bin/env python

import time
from smbus import SMBus
from threading import Thread
import atexit

_bus = None
_t_poll = None
_running = False
_last_state = 0

retries = 4

ADDR = 0x15
LEDS = [0] * 12

class Handler():
    def __init__(self):
        self.press = None
        press = None

_handler = Handler()

def _init(led_mode):
    global _t_poll, _bus, ADDR

    if _bus is not None:
        return

    _bus = SMBus(i2c_bus_id())

    errors = 0

    for x in range(retries):
        try:
            _bus.write_byte_data(ADDR, 0b00000000, 0b00010000 + led_mode)
        except IOError:
            errors += 1
            time.sleep(0.001)

    if errors == retries:
        raise RuntimeError("Unable to communicate with badge!")

    _t_poll = Thread(target=_run)
    _t_poll.daemon = True
    _t_poll.start()

    atexit.register(_quit)

def _run():
    global _bus, _running, _last_state, _handler, _adc_vals
    _running = True

    while _running:
        handler = _handler
        _curr_state = _bus.read_byte_data(ADDR, 0)
        _diff_state = _curr_state - _last_state

        if _diff_state == 128:
            if callable(handler.press):
                Thread(target=handler.press, args=(True,)).start()
                _bus.write_byte_data(ADDR, 0, _curr_state - _diff_state)

        _last_state = _curr_state

        time.sleep(0.01)

def _quit():
    global _running

    if _running:
        clear()
        show()

    _running = False
    _t_poll.join()
    _bus.write_byte_data(ADDR, 0b00000000, 0b00000000)

def _pack_leds(leds):
    return [(leds[x] & 0b1111) << 4 | (leds[x+1] & 0b1111) for x in range(0,12,2)]

def i2c_bus_id():
    """Return the I2C bus ID. It varies depending on the version of your Pi.
    """
    revision = ([l[12:-1] for l in open('/proc/cpuinfo', 'r').readlines() if l[:8] == "Revision"]+['0000'])[0]
    return 1 if int(revision, 16) >= 4 else 0

def set_led(led, brightness):
    """Set an LED to a specific brightness.
    :param led: The LED to be set, 0 to 11
    :param brightness: The brightness, from 0.0 to 1.0
    e.g. set_led(0, 1.0)
    """
    global LEDS
    brightness = int(brightness * 15.0)
    LEDS[led] = brightness

def set_all(brightness):
    """Set all of the LEDs to a specific brightness.
    :param brightness: The brightness, from 0.0 to 1.0
    e.g. set_all(1.0)
    """
    global LEDS
    brightness = int(brightness * 15.0)
    LEDS = [brightness] * 12

def clear():
    """Clears any set pixels, i.e. set them to zero brightness.
    """
    global LEDS
    LEDS = [0] * 12

def show():
    """Displays any set pixels.
    """
    global LEDS, _bus, _pack_leds, ADDR
    _init(1)
    packed = _pack_leds(LEDS)
    errors = 0

    for x in range(retries):
        try:
            _bus.write_i2c_block_data(ADDR, 0b00000001, packed)
        except IOError:
            errors += 1
            time.sleep(0.001)

    if errors == retries:
        raise RuntimeError("Unable to communicate with badge!")

def set_pattern(pattern):
    """Set the pattern of the LEDs.
    :param pattern: The pattern to be set, 0 to 11
    e.g. set_pattern(0)
    """
    _init(0)
    _bus.write_byte_data(ADDR, 0b00001000, pattern)

def on_press(handler=None):
    """Attach a press handler to the button.
    This handler is fired when you press the button.
        @bearables.on_press()
        def handler():
            # Your code here
    :param handler: Optional: a function to bind as the handler
    """
    _init(1)

    def attach_handler(handler):
        _handler.press = handler

    if handler is not None:
        attach_handler(handler)
    else:
        return attach_handler

def read_adc():
    """Return the raw ADC value across the badge's hooks (0-255).
    """
    global _bus, ADDR
    _init(1)
    return _bus.read_byte_data(ADDR, 7)

def main():
    while True:
        for i in range(12):
            set_pattern(i)
            time.sleep(5)

if __name__ == "__main__":
    main()
