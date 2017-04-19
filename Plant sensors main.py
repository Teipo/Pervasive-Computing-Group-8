import pycom
import time

pycom.heartbeat(False)

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0x7f7f00

#   Signal functions
def ok():
    pycom.rgbled(green)
    time.sleep(0.1)
    pycom.rgbled(off)
    time.sleep(2)
    return;
    
def tick():
    time.sleep(0.1)
    pycom.rgbled(red) 
    time.sleep(0.1)
    pycom.rgbled(off)
    return;
    
def tock():
    time.sleep(0.2)
    pycom.rgbled(red) 
    time.sleep(0.4)
    pycom.rgbled(off)
    return;

def sos( ):
    tick().tick().tick()
    tock().tock().tock()
    tick().tick().tick()
    time.sleep(2)           #sleep
    return;


#Chirp Scan = 32
from machine import I2C
i2c = I2C(0, I2C.MASTER, baudrate=10000)
from struct import unpack

#   Measuring functions
#   For more details on these functions, see bottom of this file
def measureTemperature():
    return (unpack('<H', i2c.readfrom_mem(0x20, 5, 2))[0]  >> 8) + ((unpack('<H', i2c.readfrom_mem(0x20, 5, 2))[0]  & 0xFF) << 8) ;
    
def measureMoisture():
    return (unpack('<H', i2c.readfrom_mem(0x20, 0, 2))[0]  >> 8) + ((unpack('<H', i2c.readfrom_mem(0x20, 0, 2))[0]  & 0xFF) << 8) ;
    
def measureLight():
    i2c.writeto(0x20, '\x03')
    time.sleep(1.5)
    return (unpack('<H', i2c.readfrom_mem(0x20, 4, 2))[0]  >> 8) + ((unpack('<H', i2c.readfrom_mem(0x20, 4, 2))[0]  & 0xFF) << 8) 
    

#   Main cycle
for cycles in range(200): # stop after 200 cycles
    temperature = measureTemperature()
    light = measureLight()
    moisture = measureMoisture()    
    print("Temperature: " + str(temperature/10) + "   Light: " + str(light) + "  Moisture: " + str(moisture)) 
    if temperature > 250 :
        ok()
    else :
        sos()
   
  
    #   i2c = I2C(0, I2C.MASTER, baudrate=10000) 
    #   print(i2c.scan())
    #   temp_reg = 5  #for temperature
    #   moisture_reg = 0 #for moisture_reg
    #   light_reg = 4 #for light
    
    #   To measure temperature and moisture
    #   a = i2c.readfrom_mem(0x20, temp_reg, 2)
    #   v = unpack('<H', a)[0]  # Should return 3329
    #   temperature = (v >> 8) + ((v & 0xFF) << 8) 
    
    #   to measure light
    #   i2c.writeto(0x20, '\x03')
    #   b = i2c.readfrom_mem(0x20, light_reg, 2)
    #   v2 = unpack('<H', b)[0]  # Should return 3329
    #  light = (v2 >> 8) + ((v2 & 0xFF) << 8) 


