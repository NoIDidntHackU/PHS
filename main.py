from machine import Pin, SoftSPI, time_pulse_us
from max7219_8digit import Display
import time

####
# Constants
##

# Constants
SPEED_SOUND=360.3 # m/s
TRIG_PULSE_DURATION_US=1 #us
DEBOUNCE_DELAY=0.05 # 50ms
COUNTER_THRESHOLD=20 # cm


######
# PIN layouts 
##

# Button Triggers
PIN_IN_CALIB = 0
PIN_IN_MEAS = 1

pin_button_1 = Pin(PIN_IN_CALIB, Pin.IN, Pin.PULL_DOWN)
pin_button_2 = Pin(PIN_IN_MEAS, Pin.IN, Pin.PULL_DOWN)    

#PINs for MAX7219 - Display
# Prototype Board -> Pico GPIO
PIN_OUT_DIN = 21
PIN_OUT_CS = 20
PIN_OUT_CLK = 19

# Breadboard Pin Mapping
#PIN_OUT_DIN = 3
#PIN_OUT_CS = 5
#PIN_OUT_CLK = 2

# TODO: Might miso is 0, this might be a conflict with 0
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(PIN_OUT_CLK), mosi=Pin(PIN_OUT_DIN), miso=Pin(0))
pin_ss = Pin(PIN_OUT_CS, Pin.OUT)
display = Display(spi, pin_ss)


# HC-SR04 Pin Mapping -> Pico
PIN_OUT_ECHO = 15  # GPIO15
PIN_IN_TRIG = 14   # GPIO14

pin_trig = Pin(PIN_OUT_ECHO, Pin.OUT) 
pin_echo = Pin(PIN_IN_TRIG, Pin.IN)  


####
# Modes of operation - Enumerated type
##
MODE_MEASURE=0
MODE_COUNTER=1
MODE_RT=2
MODE_INVALID=-1

####
# Running Variables
##
#mode = MODE_RT
mode = MODE_COUNTER

calib = -1
counter = 0


def readFromSensor(measureCount = 4, delay=5):
    """
    """
    sum = 0
    readList = []
    
    for n in range(measureCount):
        
        pin_trig.value(0)
        time.sleep_us(int(delay))
        
        # Trigger Pin for Duration
        pin_trig.value(1)
        time.sleep_us(TRIG_PULSE_DURATION_US)
        pin_trig.value(0)
                
        # TODO - look into the time_pulse_us(...) function
        ultrasonic_duration = time_pulse_us(pin_echo, 1, 30000)
        
        # TODO - what is / 20000  - conversion from m/s -> cm 
        distance_cm = SPEED_SOUND * ultrasonic_duration / 20000
        
        sum += distance_cm
   
    avg = sum / measureCount 

    return avg


def measure( samples, delay=5, wait_time=0):
    if wait_time > 0:
        time.sleep(wait_time)
        
    meas = readFromSensor(samples, delay)
    return meas


def output_display( measure, prefix="", postfix="CM"):
    out_str = "{}{:06.2f}{}".format(prefix, measure, postfix)
    print(out_str)
    display.write_to_buffer(out_str) 
    display.display()
    time.sleep_us(10)

def measure_calib():
    
    mes = measure(10, 0.1, 5)
    
    calib = mes
    
    return mes
    

def mode_realtime():
    mes = measure(5, 0.1)
    output_display(mes)
    time.sleep(0.1)
    
def mode_counter(butcal, butreset):
    global calib, counter
    
    if butreset:
        counter = 0
        output_display(counter, "C ", "")
        
    if butcal:
        calib = measure(10, wait_time=5.0)
        output_display(calib, "CAL ")
        return 
    # button press
    # measure_calib 
    
    if calib < 0:
        output_display(calib, "CAL ")
        return 
    
    mes = measure(3,0.1)
    if calib - mes > COUNTER_THRESHOLD:
        counter += 1
        
        # wait for the object to go away
        while calib - mes > COUNTER_THRESHOLD:
            mes = measure(3, 0.1)
            time.sleep(0.1)
            
        output_display(counter, "C ", "")
        
def mode_measure(butcal, butmeas):
    global calib
    # button press
    # measure calib
    if butcal:
        calib = measure(10, wait_time=5.0)
        output_display(calib, "CAL ")
        return
    
    if butmeas:
        mes =measure(5, 0.1)
        if calib < 0:
            output_display(0, "ERR CAL")
            return
        
        output_display(calib - mes)
    
def debounceSwitch(pin, in_value):
    
    out_value = in_value
    
    #check for new value
    new_value = pin.value()
    
    #simple test to check on new state
    if new_value != in_value:
        # new state to the debounce
        time.sleep(DEBOUNCE_DELAY)
            
        out_value = pin.value()
        
    
    return out_value
            
        

######
# Main Loop 
#

print(f"DEBUG: mode={mode}")
output_display(mode,f"mode ","")

butState_1 = pin_button_1.value()
butState_2 = pin_button_2.value()

#while False:
while True:
    
    but_1 = debounceSwitch(pin_button_1, butState_1)
    but_2 = debounceSwitch(pin_button_2, butState_2)
    
    but_1_change = but_1 != butState_1
    but_2_change = but_2 != butState_2
    
    if but_1_change or but_2_change:
        print(f"Button 1 {but_1_change} Button 2 {but_2_change}")
    
    if mode == MODE_MEASURE:
        mode_measure(but_1_change, but_2_change)
        pass
    elif mode == MODE_COUNTER:
        mode_counter(but_1_change, but_2_change)
        pass
    elif mode == MODE_RT:
        mode_realtime()
        pass
    else:
        print(f"ERROR - Invalid mode")