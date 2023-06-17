from machine import Pin, SoftSPI
import max7219_8digit


spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0))
ss = Pin(5, Pin.OUT)
display = max7219_8digit.Display(spi, ss)

display.write_to_buffer("12.34")
display.display()
