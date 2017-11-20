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
