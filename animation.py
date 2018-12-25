"""TLC5957 & FancyLED."""

__doc__ = """
animation.py - TLC5957 & FancyLED & 2D Array / Mapping.

this is sub file for the magic amulet animation things.
it combines the TLC5957 library with FancyLED and 2D Array / Mapping.

Enjoy the colors :-)
"""

import board
# import busio
import bitbangio
import pulseio
import digitalio

import slight_tlc5957
import adafruit_fancyled.adafruit_fancyled as fancyled


##########################################
if __name__ == '__main__':
    print(
        "\n" +
        (42 * '*') + "\n" +
        __doc__ + "\n" +
        (42 * '*') + "\n" +
        "\n"
    )

##########################################
print(42 * '*')
print("initialise digitalio pins for SPI")
spi_clock = digitalio.DigitalInOut(board.SCK)
spi_clock.direction = digitalio.Direction.OUTPUT
spi_mosi = digitalio.DigitalInOut(board.MOSI)
spi_mosi.direction = digitalio.Direction.OUTPUT
spi_miso = digitalio.DigitalInOut(board.MISO)
spi_miso.direction = digitalio.Direction.INPUT

# print((42 * '*') + "\n" + "init busio.SPI")
# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
print("init bitbangio.SPI")
spi = bitbangio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# on the ItsyBitsy M4 EXPRESS on pin D9 the maximum frequency is about 6MHz?!
# gsclk_freqency = (6 * 1000 * 1000)  # 6MHz
gsclk_freqency = (20 * 1000 * 1000)  # 10MHz
gsclk = pulseio.PWMOut(
    board.D9, duty_cycle=(2 ** 15), frequency=gsclk_freqency)
print("gsclk.frequency: {:}MHz".format(gsclk.frequency / (1000*1000)))

latch = digitalio.DigitalInOut(board.D7)
latch.direction = digitalio.Direction.OUTPUT

##########################################
print(42 * '*')
print("define pixel array / init TLC5957")
LEDBoard_count = 3
LEDBoard_row_count = 4
LEDBoard_col_count = 4
pixel_col_count = LEDBoard_count * LEDBoard_col_count
pixel_count = pixel_col_count * LEDBoard_row_count
pixels = slight_tlc5957.TLC5957(
    spi=spi,
    latch=latch,
    gsclk=gsclk,
    spi_clock=spi_clock,
    spi_mosi=spi_mosi,
    spi_miso=spi_miso,
    pixel_count=pixel_count)

# How to map a 2D-Pixel Array to the needed TLC5957 sending order:
#
# physically the pixels are orderd this way on the board:
# physical_map = [
#     [ 0,  1,  2,  3],
#     [ 4,  5,  6,  7],
#     [ 8,  9, 10, 11],
#     [12, 13, 14, 15],
# ]
# but we need to reverse this order for the send data.
# this results in
# pixel_map = [
#     [15, 14, 13, 12],
#     [11, 10,  9,  8],
#     [ 7,  6,  5,  4],
#     [ 3,  2,  1,  0],
# ]
# if we have more than one chip it gets a little bit complicated.
# we need to first send all physical last pixels in one row.
# than the next and so on..
# so if we have a physical map with 2*16 LEDs:
# physical_map = [
#      CHIP_1            CHIP_2
#     [ 0,  1,  2,  3,    0,  1,  2,  3],
#     [ 4,  5,  6,  7,    4,  5,  6,  7],
#     [ 8,  9, 10, 11,    8,  9, 10, 11],
#     [12, 13, 14, 15,   12, 13, 14, 15],
# ]
# this results in this pixel-sending order:
# pixel_map = [
#      CHIP_1            CHIP_2
#     [31, 29, 27, 25,   30, 28, 26, 24],
#     [23, 21, 19, 17,   22, 20, 18, 16],
#     [15, 13, 11,  9,   14, 12, 10,  8],
#     [ 7,  5,  3,  1,    6,  4,  2,  0],
# ]


LEDBoard_map = [
    [15, 14, 13, 12],
    [11, 10,  9,  8],
    [7,   6,  5,  4],
    [3,   2,  1,  0],
]

# create empty 2d list
# this will be filled by the initialisation for all chips/pcbs
pixel_map = [
    [0 for c in range(pixel_col_count)] for r in range(LEDBoard_row_count)
]
# print(pixel_map)


def pixel_map_fill():
    """."""
    index_offset = 0

    print(
        "|----------index----------|-----------map----------|\n"
        "| board | row | col | cwb | offset | board | pixel |"
    )
    for board_index in range(LEDBoard_count):
        for row_index in range(LEDBoard_row_count):
            for col_index in range(LEDBoard_col_count):
                col_index_w_board = col_index * board_index
                # set new pixel_index
                pixel_map[row_index][col_index_w_board] = (
                    index_offset + LEDBoard_map[row_index][col_index])
                # print debug things
                print(
                    "| "
                    "{board:^5} | "
                    "{row:^3} | "
                    "{col:^3} | "
                    "{col_w_board:^3} | "
                    "{index_offset:^6} | "
                    "{board_map:^5} | "
                    "{pixel_map:^5} | "
                    "".format(
                        board=board_index,
                        col=col_index,
                        row=row_index,
                        col_w_board=col_index_w_board,
                        index_offset=index_offset,
                        board_map=LEDBoard_map[row_index][col_index],
                        pixel_map=pixel_map[row_index][col_index_w_board],
                    )
                )

        # prepare next board
        index_offset += pixels.CHIP_LED_COUNT
    print("|--------------------------------------------------|")

# pixel_map_fill()


def pixel_map_print_information():
    """Print all Information regarding pixel_map."""
    print(
        "Pixels & Mapping:\n"
        "  LEDBoard_count {LEDBoard_count:>2}\n"
        "  LEDBoard_row_count           {LEDBoard_row_count:>2}\n"
        "  LEDBoard_col_count           {LEDBoard_col_count:>2}\n"
        "  pixel_count    {pixel_count:>2}\n"
        "  chip_count     {chip_count:>2}\n"
        "  channel_count  {channel_count:>2}\n"
        "".format(
            LEDBoard_count=LEDBoard_count,
            LEDBoard_row_count=LEDBoard_row_count,
            LEDBoard_col_count=LEDBoard_col_count,
            pixel_count=pixels.pixel_count,
            chip_count=pixels.chip_count,
            channel_count=pixels.channel_count,
        )
    )
    print(pixel_map)


##########################################
# helper function

def map_range(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range_int(x, in_min, in_max, out_min, out_max):
    """Map Value from one range to another."""
    return int(
        (x - in_min) * (out_max - out_min)
        //
        (in_max - in_min) + out_min
    )


##########################################
# mapping function

def get_pixel_index_from_row_col(row, col):
    """Get pixel_index from row and column index."""
    pixel_index = pixel_map[row][col]
    return pixel_index


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

def test_set_corners_to_colors():
    """Test Function: Set all 4 corners to different collors."""
    print(42 * '*')
    print("set corners to colors")
    pixels[get_pixel_index_from_row_col(0, 0)] = (1.0, 0.5, 0.0)
    pixels[get_pixel_index_from_row_col(0, 3)] = (0.5, 0.0, 1.0)
    pixels[get_pixel_index_from_row_col(3, 0)] = (0.1, 0.5, 0.0)
    pixels[get_pixel_index_from_row_col(3, 3)] = (0.0, 0.5, 1.0)
    pixels.show()


def test_set_2d_colors():
    """Test Function: Set all LEDs to 2D color-range."""
    print("set color range")
    for x in range(LEDBoard_col_count):
        # xN = x / LEDBoard_col_count
        xN = map_range_int(x, 0, LEDBoard_col_count, 1, 100)
        for y in range(LEDBoard_row_count):
            # yN = y / LEDBoard_row_count
            yN = map_range_int(y, 0, LEDBoard_row_count, 1, 100)
            # print(
            #     "x: {:>2} xN: {:>2} "
            #     "y: {:>2} yN: {:>2} "
            #     "pixel_index: {:>2}".format(
            #         x, xN,
            #         y, yN,
            #         get_pixel_index_from_row_col(x, y)
            #     )
            # )
            pixels[get_pixel_index_from_row_col(x, y)] = (xN, yN, 0)

    pixels.show()


def test_loop_2d_colors():
    """Test Function: Set all LEDs to 2D color-range."""
    # Positional offset for blue part
    offset = 0
    print(42 * '*')
    print("loop")
    while True:
        offsetN = map_range_int(offset, 0.0, 1.0, 1, 200)
        for x in range(LEDBoard_col_count):
            xN = map_range_int(x, 0, LEDBoard_col_count, 1, 500)
            for y in range(LEDBoard_row_count):
                yN = map_range_int(y, 0, LEDBoard_row_count, 1, 500)
                pixels[get_pixel_index_from_row_col(x, y)] = (xN, yN, offsetN)
        pixels.show()
        offset += 0.01  # Bigger number = faster spin
        if offset > 1.0:
            offset = 0


def test_main():
    """Test Main."""
    import time

    test_set_corners_to_colors()
    time.sleep(10)
    test_set_2d_colors()
    time.sleep(10)
    test_loop_2d_colors()


##########################################
# main loop

if __name__ == '__main__':
    test_main()
