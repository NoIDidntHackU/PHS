# read from Distance sensor (Jonboan?):






# ************************************************

# write to 8 digit 7 segment display (NoIDidntHackU):
# Schematic:
# schematic7sgmnt.png
#  (for some reason doesn't work, not too sure why. maybe you could check it?)
# ********************REQUIRED********************
# MicroPython library for MAX7219 + 8 x 7digit display boards.

# Download the max7219_8digit.py library

# Open the RPi Pico as drive, and then copy the library into root directory.

# The library provides

# -- Initializing the device

# -- Set intensity of the device

# -- Write To Buffer functionality

# -- Send the buffer to MAX7219 device for further processing.
# ************************************************

# Example of use:

# Connections:
# SCK (CLK) -> GPIO4 (D2)
# MOSI (DIN) -> GPIO2 (D4)
# SS (CS) -> GPIO5 (D1)

from machine import Pin, SPI
#import max7219_8digit
import max7219

# the max7219 doesn't use the MISO, but unfortunately SoftSPI requires that
# we specify it anyway
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2), miso=Pin(0))

ss = Pin(5, Pin.OUT)

display = max7219_8digit.Display(spi, ss)
display.write_to_buffer('12345678')
display.display()

#************************************************
#There is also a write_to_buffer_with_dots method, which attempts to use the display decimal points properly. Note that there are some rather big bugs in this at the moment, do not put dots at the start of the string, or put two of them in a row.

# Connections:
# SCK (CLK) -> GPIO4 (D2)
# MOSI (DIN) -> GPIO2 (D4)
# SS (CS) -> GPIO5 (D1)

from machine import Pin, SPI
import max7219_8digit

spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2), miso=Pin(0))

ss = Pin(5, Pin.OUT)

display = max7219_8digit.Display(spi, ss)
display.write_to_buffer_with_dots('1234.56.78')
display.display()

#************************************************
