#
# Taken from https://www.instructables.com/How-to-Connect-HC-SR04-Ultrasonic-With-Raspberry-P/
#

from machine import Pin, time_pulse_us
import time


SPEED_SOUND=340 # m/s
TRIG_PULSE_DURATION_US=10 #us

trig_pin = Pin(15, Pin.OUT) # GPIO15
echo_pin = Pin(14, Pin.IN)  # GPIO14

measure_count = 4

def ultra():
    
    for n in range(measure_count):
        
        trig_pin.value(0)
        time.sleep_us(5)
        
        # Trigger Pin for Duration
        trig_pin.value(1)
        time.sleep_us(TRIG_PULSE_DURATION_US)
        trig_pin.value(0)
        
        # TODO - look into the time_pulse_us(...) function
        ultrasonic_duration = time_pulse_us(echo_pin, 1, 30000)
        
        # TODO - what is / 20000  - conversion from m/s -> cm 
        distance_cm = SPEED_SOUND * ultrasonic_duration / 20000
        
        print(f"Distance = {distance_cm} cm")
        