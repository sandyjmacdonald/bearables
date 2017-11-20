# Bearables

The Pimoroni [Bearables badges](https://shop.pimoroni.com/collections/bearables) include an I2C interface via the 5 programming pads on the reverse of the badges allowing basic control of the LED patterns, the individual LEDs, the button, and the ADC reading across the hooks when connected to a sensor, for example. This library exposes those functions.

## Installation

To install the Bearables library, open a terminal window, and type the following:

```
git clone https://github.com/sandyjmacdonald/bearables.git
cd bearables/library
sudo python3 setup.py install
```

Note that the installation requires the `smbus` library.

## Interfacing

The 5 pads on the reverse of the badges, just below the Bearables logo, are used for programming the PIC microprocessor, but can also be used to power the badge and interface with it via I2C. If you're powering it through the 3V3 pin of your Pi or microprocessor, then make sure that you don't also have a battery in your badge.

The pads, from left to right, are as follows:

* 9V reset
* SDA
* SCL
* GND
* 3V3

The easiest way to connect the badge to your Pi's GPIO is with a piece of right-angled male header soldered to the pads, and some female to female jumper jerky. Connect the SDA and SCL pins to your Pi's [SDA and SCL pins](https://pinout.xyz/pinout/i2c) and the 3V3 and GND to 3V3 power and ground respectively.

The badge should light up when connected. You can check that the I2C is being detected by typing `sudo i2cdetect -y 1`. It should show up with address `0x15`.

## Examples

There are a number of examples in the [bearables/examples](examples) directory.

## Functionality

### LED patterns

The `set_pattern()` function allows you to select one of the 12 preset patterns on the badge, numbered from 0 to 11.

```
import time
from bearables import set_pattern

while True:
    for i in range(12):
        set_pattern(i)
        time.sleep(5)
```

### LED control

The `set_led()`, `set_all()`, `show()`, and `clear()` functions allow control of the LEDs, for programming your own patterns. The `show()` function must always be called after setting or clearing any LEDs, to display the changes on the badge's LEDs.

Here's an example of how to cycle round the badge's LEDs at full brightness:

```
import time
from bearables import set_led, show, clear

while True:
    for i in range(12):
        clear()
        set_led(i, 1.0)
        show()
        time.sleep(0.05)
```

The `set_led()` function takes two arguments, the LED number from `0` to `11`, and a brightness value from `0.0` to `1.0`. There's also a `set_all()` function that takes a single argument, the brightness value from `0.0` to `1.0`.

### Button

Button press events can be linked to functions using the `@on_press` decorator. The function to which the decorator is attached will fire every time the button is pressed. Here's an example that turns all of the LEDs on for two seconds when the button is pressed:

```
import time
from bearables import set_all, show, clear, on_press

@on_press
def handle_press(self):
    set_all(1.0)
    show()
    print("Button pressed!!")
    time.sleep(2)
    clear()
    show()

while True:
    pass
```
