"""TLC5971 & FancyLED."""

__doc__ = """
animation.py - TLC5971 & FancyLED & 2D Array / Mapping.

it combines the TLC5971 library with FancyLED and 2D Array / Mapping.

(see [LEDBoard_4x4_16bit](https://github.com/s-light/LEDBoard_4x4_16bit)
for the aktuall hardware used..)

Enjoy the colors :-)
"""

import time

import board
import busio

# from adafruit_tlc59711.adafruit_tlc59711 import TLC59711
from adafruit_tlc59711.adafruit_tlc59711_multi import TLC59711Multi
import adafruit_fancyled.adafruit_fancyled as fancyled


##########################################
if __name__ == '__main__':
    print()
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print()

##########################################
print(42 * '*')
print("define pixel array / init TLC5971")

LEDBoard_count = 8
# LEDBoard_count = 1
LEDBoard_row_count = 4
LEDBoard_col_count = 4
pixel_col_count = LEDBoard_count * LEDBoard_col_count
pixel_count = pixel_col_count * LEDBoard_row_count

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = TLC59711Multi(spi, pixel_count=pixel_count)


##########################################
# helper function

# def map_01_to_16bit(color):
#     """Map range 0..1 to 16bit 0..65535."""
#     return (
#         int(color.red * 65535),
#         int(color.green * 65535),
#         int(color.blue * 65535)
#     )


##########################################
# Declare a 6-element RGB rainbow palette
palette = [
    fancyled.CRGB(1.0, 0.0, 0.0),  # Red
    fancyled.CRGB(0.5, 0.5, 0.0),  # Yellow
    fancyled.CRGB(0.0, 1.0, 0.0),  # Green
    fancyled.CRGB(0.0, 0.5, 0.5),  # Cyan
    fancyled.CRGB(0.0, 0.0, 1.0),  # Blue
    fancyled.CRGB(0.5, 0.0, 0.5),  # Magenta
]


##########################################
# test functions

# Positional offset into color palette to get it to 'spin'
offset = 0

value_high = 2000


def rainbow_update():
    """Rainbow."""
    global offset
    for i in range(pixel_count):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancyled.palette_lookup(palette, offset + i / pixel_count)
        color = fancyled.gamma_adjust(color, brightness=0.25)
        # print("{index:>2} : {div:>2} | {mod:>2}".format(
        #     index=i,
        #     div=i // 4,
        #     mod=i % 4
        # ))
        # pixels[i // 4][i % 4] = map_01_to_16bit(color)
        pixels[i] = color
    pixels.show()

    offset += 0.001  # Bigger number = faster spin


def channelcheck_update():
    """ChannelCheck."""
    global offset
    # print("offset", offset)
    # i_prev = i - 1
    # pixels[i_prev // 4][i_prev % 4] = (0, 0, 0)
    pixels[offset] = (value_high, 0, 0)
    # pixels[i // 4][i % 4] = (value_high, 0, 0)
    pixels.show()
    offset += 1
    if offset >= pixel_count:
        offset = 0
        set_all_black()


def set_all_black():
    """Set all Pixel to Black."""
    set_all((0, 0, 0))


def set_all(color):
    """Set all Pixel to color."""
    for i in range(pixel_count):
        # pixels[i // 4][i % 4] = color
        pixels[i] = color


def flash_fade():
    """Set all Pixel to color."""
    top = 60000
    # duration = 5
    # step_duration = duration / top
    # fade up
    for i in range(0, top // 6, 1000):
        set_all((i, i, i))
        pixels.show()
    for i in range(top // 6, top, 5000):
        set_all((i, i, i))
        pixels.show()
        # time.sleep(step_duration)
    # wait...
    time.sleep(1)
    # reset
    set_all_black()
    pixels.show()


def flash():
    """Set all Pixel to color."""
    top = 60000
    set_all((top, top, top))
    pixels.show()
    # wait...
    time.sleep(1)
    # reset
    set_all_black()
    pixels.show()


def test_main():
    """Test Main."""
    import time

    time.sleep(1)

    while True:
        rainbow_update()


##########################################
# main loop

if __name__ == '__main__':
    test_main()
