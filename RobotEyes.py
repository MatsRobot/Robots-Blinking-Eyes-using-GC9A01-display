import random
from machine import Pin, SPI
import gc9a01py as gc9a01
import framebuf
import time


# RST = GP4
# CS = GP6
# DC = GP5
# SDA = GP3
# SCL = GP2
# GND = GND
# VCC = 3V3 out



spi = SPI(0, baudrate=20000000, sck=Pin(2), mosi=Pin(3))
tft = gc9a01.GC9A01(
    spi,
    dc=Pin(5, Pin.OUT),
    cs=Pin(6, Pin.OUT),
    reset=Pin(4, Pin.OUT),
    backlight=Pin(15, Pin.OUT),
    rotation=2)

tft.fill(0xFFFF)


# Open the image file and read the header
# eye_iris_RGB-128x128.bmp

with open('eye_iris_RGB-128x128.bmp', 'rb') as f:
    f.seek(18)
    width = int.from_bytes(f.read(4), 'little')
    height = int.from_bytes(f.read(4), 'little')
    print(width, height)
    
    offset = 54 #int.from_bytes(f.read(4), 'little')
    #width = 128 #int.from_bytes(f.read(4), 'little')
    #height = 128 #int.from_bytes(f.read(4), 'little')

    # Create a frame buffer for the image
    buf = bytearray(width * height * 2)
    fb = framebuf.FrameBuffer(buf, width, height, framebuf.RGB565)

# Read the image data and draw it to the screen
    f.seek(offset)
    for y in range(height):
        row = bytearray(f.read(width * 3))
        for x in range(width // 2):
            i = x * 3
            j = (width - x - 1) * 3
            row[i:i+3], row[j:j+3] = row[j:j+3], row[i:i+3]
        for x in range(width):
            b = row[x*3]
            r = row[x*3+1]
            g = row[x*3+2]
            fb.pixel(x, y, (b << 8) | (g << 3) | (r >> 3))
            
while True:
    tft.blit_buffer(buf, 58 + random.randint(-30, 30), 58 + random.randint(-30, 30), width, height)
    time.sleep(random.randrange(1, 2))
    tft.fill(0xFFFF)
    tft.blit_buffer(buf, 58 , 58 , width, height) # Centre the eye
    time.sleep(random.randrange(1, 4))
    tft.fill(0xFFFF)
    time.sleep(0.1)
