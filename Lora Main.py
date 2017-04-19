import pycom
import time
import network
import binascii
import socket

from network import LoRa

wlan = network.WLAN()
print(wlan.ssid())
print(wlan.mode)

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0x7f7f00

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


s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

i = 0
bytes = bytearray(3)
light = 15356
light_id = 0xCC

while True:
    bytes[0] = light_id
    bytes[1] = (light & 0xFF00) >> 8
    bytes[2] = (light & 0x00FF)
    count = s.send(bytes)
    print('Sent %s bytes' % count)
    pycom.rgbled(green)
    time.sleep(0.1)
    pycom.rgbled(blue)
    time.sleep(9.9)
    i += 1

