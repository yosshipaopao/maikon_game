from busio import SPI
from board import SCK, MOSI, MISO, D8, D18, D23, D24, D2, D3
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display.ili9341 import ILI9341
from PIL import Image, ImageDraw
import cv2
import os
CS_PIN    = DigitalInOut(D8)
LED_PIN   = DigitalInOut(D18)
RESET_PIN = DigitalInOut(D23)
DC_PIN    = DigitalInOut(D24)
LED_PIN.direction = Direction.OUTPUT

SWITCH_PIN = DigitalInOut(D3)
SWITCH_PIN.direction = Direction.INPUT

UDP_SHUTDOWN_SH_PORT=50001

spi = SPI(clock=SCK, MOSI=MOSI, MISO=MISO)
display = ILI9341(
    spi,
    cs = CS_PIN,
    dc = DC_PIN,
    rst = RESET_PIN,
    width = 240,
    height = 320,
    rotation = 90,
    
    baudrate=24000000)
def display_img(filename, error_mark=False):
    if not (os.path.isfile(filename)):
        print("error")
        return
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (320, 240),  interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if error_mark:
        cv2.rectangle(img, (0, 0), (2, 2), (255, 255, 255), thickness=-1)
    frame = Image.fromarray(img)
    display.image(frame)
display_img("screen.png")