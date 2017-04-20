import pycom
import time
import network
import binascii
import socket
from network import LoRa
from network import Bluetooth

wlan = network.WLAN()
#print(wlan.ssid())
#print(wlan.mode)

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0x7f7f00


Bluetooth = Bluetooth()
Bluetooth.stop_scan()
Bluetooth.disconnect_client()

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.disconnect()
print("WLAN connected: " + str(wlan.isconnected()))
print("Bluebooth scanning: " + str(Bluetooth.isscanning()))


#   Signal functions
def ok():
    pycom.rgbled(green)
    time.sleep(0.3)
    pycom.rgbled(off)
    time.sleep(2)
    pycom.rgbled(green)
    time.sleep(0.3)
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
    tick()
    tick()
    tick()
    tock()
    tock()
    tock()
    tick()
    tick()
    tick()
    time.sleep(2)           #sleep
    return;

pycom.heartbeat(False)
lora = LoRa(mode=LoRa.LORAWAN)

#   print(binascii.hexlify(lora.mac()).upper().decode('utf-8'))
#   Set network keys
app_eui = binascii.unhexlify('70B3D57EF0003F19')
app_key = binascii.unhexlify('D6F26B67C1ED1E76AD1AD9A7227222AB')

# Join the network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
pycom.rgbled(red)

# Loop until joined
while not lora.has_joined():
    print('Not joined yet...')
    pycom.rgbled(off)
    time.sleep(0.1)
    pycom.rgbled(red)  # tick
    time.sleep(2)           #sleep

print('Joined')
pycom.rgbled(blue)
time.sleep(3)

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

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

# https://github.com/ITU-PerCom-2017/resources/blob/master/assignment01/backend/README.md
light_bytes = bytearray(3)
light_bytes[0] = 0xCC   #   ID of the light

temperature_bytes = bytearray(3)
temperature_bytes[0] = 0xAA   #   ID of the temperature

moisture_bytes = bytearray(3)
moisture_bytes[0] = 0xBB   #   ID of the moisture

pycom.rgbled(off)

i = 0

while True:
    pycom.rgbled(blue)
    time.sleep(0.3)
    pycom.rgbled(off)
    temperature = measureTemperature()
    moisture = measureMoisture()
    light = measureLight()

    light_bytes[1] = (light & 0xFF00) >> 8
    light_bytes[2] = (light & 0x00FF)

    moisture_bytes[1] = (moisture & 0xFF00) >> 8
    moisture_bytes[2] = (moisture & 0x00FF)

    temperature_bytes[1] = (temperature & 0xFF00) >> 8
    temperature_bytes[2] = (temperature & 0x00FF)

    light_count = s.send(light_bytes)
    temperature_count = s.send(temperature_bytes)
    moisture_count = s.send(moisture_bytes)

    print('Sent %s light_bytes' % light_count)
    print("Temperature: " + str(temperature/10) + "   Light: " + str(light) + "  Moisture: " + str(moisture))
    i = i + 3

    print("Packages: " + str(i))
    pycom.rgbled(green)
    time.sleep(0.3)
    pycom.rgbled(off)
    time.sleep(10)
