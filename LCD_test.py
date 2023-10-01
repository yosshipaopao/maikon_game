from busio import SPI
from board import SCK, MOSI, MISO, D8, D18, D23, D24, D3
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display.ili9341 import ILI9341
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
def display_img(image):
    display.image(image)
display_img("screen.png")