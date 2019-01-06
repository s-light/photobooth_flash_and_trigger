"""TLC5971 & FancyLED."""

__doc__ = """
animation.py - TLC5971 & FancyLED & 2D Array / Mapping.

it combines the TLC5971 library with FancyLED and 2D Array / Mapping.

Enjoy the colors :-)
"""

import time

import board
import busio

from adafruit_tlc59711.adafruit_tlc59711_multi import TLC59711Multi
import adafruit_fancyled.adafruit_fancyled as fancyled
from pixel_map import PixelMap2D


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


# How to map a 2D-Pixel Array to the needed TLC5971 sending order:


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
                    index_offset + LEDBoard_single[row_index][col_index])
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
                        board_map=LEDBoard_single[row_index][col_index],
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
# mappings

LEDBoard_row_count = 4
LEDBoard_col_count = 4
LEDBoard_pixel_count = LEDBoard_row_count * LEDBoard_col_count
LEDBoard_single = [
    [4, 5, 12, 13],
    [6, 7, 14, 15],
    [0, 1, 8, 11],
    [2, 3, 10, 12],
]

Boards_row_count = 4
Boards_col_count = 2
Boards_positions = [
    [4, 8],
    [3, 7],
    [2, 6],
    [1, 5],
]

matrix_col_count = LEDBoard_col_count * Boards_col_count
matrix_row_count = LEDBoard_row_count * Boards_row_count


def mymap_LEDBoard_4x4_16bit(self, row, col):
    """Map row and col to pixel_index."""

    Board_count = self.pixel_count // LEDBoard_pixel_count

    # physical_index = (row * self.col_count) + col

    # row_inv = (self.row_count-1) - row
    col_inv = (self.col_count - 1) - col

    # split chip position from chip_inner
    chipin_row = row % LEDBoard_row_count
    chipin_col = col % LEDBoard_col_count
    # chip_row_inv = row_inv // LEDBoard_row_count
    chip_col_inv = col_inv // LEDBoard_col_count

    chipin_row_inv = (LEDBoard_row_count - 1) - chipin_row
    chipin_col_inv = (LEDBoard_col_count - 1) - chipin_col
    chipin_pixel_index = (
        (chipin_row_inv * LEDBoard_col_count) + chipin_col_inv
    )

    pixel_index = (chipin_pixel_index * Board_count) + chip_col_inv

    return pixel_index

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
    test_set_corners_to_colors()
    time.sleep(10)
    test_set_2d_colors()
    time.sleep(10)
    test_loop_2d_colors()


def test_map():
    """Test Map."""
    #####################
    # LEDBoard_4x4_16bit mapping

    pmap = PixelMap2D(
        row_count=matrix_row_count,
        col_count=matrix_col_count,
        map_function=mymap_LEDBoard_4x4_16bit)
    pmap.print_mapping()


##########################################
# main loop

if __name__ == '__main__':
    # test_main()
    test_map()
