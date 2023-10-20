from machine import Pin, SoftSPI, time_pulse_us
import max7219_8digit
import time

number = 99999950
distance = 0
readList = []

spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0))
ss = Pin(5, Pin.OUT)
display = max7219_8digit.Display(spi, ss)
sum = 0
SPEED_SOUND=360.3 # m/s
TRIG_PULSE_DURATION_US=0 #us

trig_pin = Pin(15, Pin.OUT) # GPIO15
echo_pin = Pin(14, Pin.IN)  # GPIO14


def readFromSensor(measureCount = 4):
    sum = 0
    readList = []
    
    for n in range(measureCount):
        
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
        
        
        readList.append(distance_cm)
        
        
    for entry in readList:
        sum = sum + entry
    
    avg = sum/len(readList)
    print(avg)
    return avg

    
    

def writeToDisplay(Output = "Nothing"):
    
        print(f"Distance = {Output}")
    
    
        display.write_to_buffer(Output) 
        display.display()
    
        time.sleep_us(TRIG_PULSE_DURATION_US)

while True:
    
    #readFromSensor()
    distance = readFromSensor(measureCount = 10)
    writeToDisplay(Output = "{:06.2f}CM".format(distance))
    #"{:08.2f}".format(number)
    
    time.sleep(1)