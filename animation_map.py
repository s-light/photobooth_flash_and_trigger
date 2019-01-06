"""TLC5971 & FancyLED."""

__doc__ = """
animation.py - TLC5971 & FancyLED & 2D Array / Mapping.

it combines the TLC5971 library with FancyLED and 2D Array / Mapping.

Enjoy the colors :-)
"""

import time

import board
import busio
import supervisor

from adafruit_tlc59711.adafruit_tlc59711_multi import TLC59711Multi
# import adafruit_fancyled.adafruit_fancyled as fancyled
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

##########################################
# mappings
# LEDBoard_4x4_16bit mapping

LEDBoard_col_count = 4
LEDBoard_row_count = 4
LEDBoard_pixel_count = LEDBoard_row_count * LEDBoard_col_count
LEDBoard_single = [
    [15, 14, 11, 10],
    [13, 12, 9, 8],
    [7, 6, 3, 2],
    [5, 4, 1, 0],
]

Boards_col_count = 2
Boards_row_count = 4
Boards_count = Boards_col_count * Boards_row_count
Boards_positions = [
    [4, 0],
    [5, 1],
    [6, 2],
    [7, 3],
]

Matrix_col_count = LEDBoard_col_count * Boards_col_count
Matrix_row_count = LEDBoard_row_count * Boards_row_count
Matrix_pixel_count = Matrix_col_count * Matrix_row_count


def mymap_LEDBoard_4x4_16bit(self, *, col=0, row=0):
    """Map row and col to pixel_index."""
    # get Board position
    board_col = col // LEDBoard_col_count
    board_row = row // LEDBoard_row_count
    board_sub_col = col % LEDBoard_col_count
    board_sub_row = row % LEDBoard_row_count
    # print(
    #     "      col:row\n"
    #     "in    {:>3}:{:>3}\n"
    #     "board {:>3}:{:>3}\n"
    #     "sub   {:>3}:{:>3}\n"
    #     "".format(
    #         col,
    #         row,
    #         board_col,
    #         board_row,
    #         board_sub_col,
    #         board_sub_row,
    #     )
    # )

    board_offset = Boards_positions[board_row][board_col]
    pixel_offset = LEDBoard_single[board_sub_row][board_sub_col]

    pixel_index = (board_offset * LEDBoard_pixel_count) + pixel_offset

    return pixel_index


pmap = PixelMap2D(
    row_count=Matrix_row_count,
    col_count=Matrix_col_count,
    map_function=mymap_LEDBoard_4x4_16bit
)

##########################################
# led controller

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = TLC59711Multi(spi, pixel_count=Matrix_pixel_count)


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


def wait_with_print(duration=1):
    """Wait with print."""
    step_duration = 0.5
    waiting_duration = 0
    while waiting_duration < duration:
        # print(". ", end='', flush=True)
        print(".", end='')
        time.sleep(step_duration)
        waiting_duration += step_duration
    print("")


##########################################

class AnimationHelper(object):
    """AnimationHelper."""

    def __init__(self):
        """Init."""
        super(AnimationHelper, self).__init__()
        self.offset = 0
        self.animation_run = True

    ##########################################
    # test functions

    @staticmethod
    def test_set_corners_to_colors():
        """Test Function: Set all 4 corners to different collors."""
        print(42 * '*')
        print("set corners to colors")
        pixels[pmap.map(
            col=0,
            row=0
        )] = (0.2, 0.05, 0.0)
        pixels[pmap.map(
            col=0,
            row=Matrix_row_count-1
        )] = (0.1, 0.0, 0.2)
        pixels[pmap.map(
            col=Matrix_col_count-1,
            row=0
        )] = (0.1, 0.2, 0.0)
        pixels[pmap.map(
            col=Matrix_col_count-1,
            row=Matrix_row_count-1
        )] = (0.0, 0.1, 0.2)
        # print("{:>3}:{:>3} = {:>3}".format(0, 0, pmap.map(0, 0)))
        # print("{:>3}:{:>3} = {:>3}".format(0, 7, pmap.map(0, 7)))
        # print("{:>3}:{:>3} = {:>3}".format(15, 0, pmap.map(15, 0)))
        # print("{:>3}:{:>3} = {:>3}".format(15, 7, pmap.map(15, 7)))
        # pixels[pmap.map(0, 0)] = (0.1, 0.01, 0.0)
        # pixels[pmap.map(0, 7)] = (0.01, 0.0, 0.1)
        # pixels[pmap.map(15, 0)] = (0.01, 0.01, 0.0)
        # pixels[pmap.map(15, 7)] = (0.0, 0.01, 0.1)
        pixels.show()

    @staticmethod
    def test_set_2d_colors():
        """Test Function: Set all LEDs to 2D color-range."""
        print("set color range")
        for x in range(Matrix_col_count):
            # xN = x / Matrix_col_count
            xN = map_range_int(x, 0, Matrix_col_count, 1, 500)
            for y in range(Matrix_row_count):
                # yN = y / Matrix_row_count
                yN = map_range_int(y, 0, Matrix_row_count, 1, 500)
                # print(
                #     "x: {:>2} xN: {:>2} "
                #     "y: {:>2} yN: {:>2} "
                #     "pixel_index: {:>2}".format(
                #         x, xN,
                #         y, yN,
                #         get_pixel_index_from_row_col(x, y)
                #     )
                # )
                pixel_index = 0
                try:
                    pixel_index = pmap.map(col=x, row=y)
                except IndexError as e:
                    print("{}; col:{col} row:{row}".format(e, col=x, row=y))
                pixels[pixel_index] = (xN, yN, 0)

        pixels.show()

    def test_loop_2d_colors(self):
        """Test Function: Set all LEDs to 2D color-range."""
        # Positional offset for blue part
        offsetN = map_range_int(self.offset, 0.0, 1.0, 1, 1000)
        for x in range(Matrix_col_count):
            xN = map_range_int(x, 0, Matrix_col_count, 1, 2000)
            for y in range(Matrix_row_count):
                yN = map_range_int(y, 0, Matrix_row_count, 1, 2000)
                pixels[pmap.map(col=x, row=y)] = (xN, yN, offsetN)
        pixels.show()
        self.offset += 0.001  # Bigger number = faster spin
        if self.offset > 1.0:
            self.offset = 0

    @staticmethod
    def handle_pixel_set(input_string):
        """Handle Pixel Set."""
        pixel = 0
        value = 0
        sep = input_string.find(":")
        try:
            pixel = int(input_string[1:sep])
        except ValueError as e:
            print("Exception parsing 'pixel': ", e)
        try:
            value = int(input_string[sep+1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        pixels.set_pixel_16bit_value(pixel, value, value, value)
        pixels.show()

    @staticmethod
    def handle_pixel_map_set(input_string):
        """Handle Pixel Set."""
        row = 0
        col = 0
        value = 0

        sep_pos = input_string.find(",")
        sep_value = input_string.find(":")
        try:
            col = int(input_string[1:sep_pos])
        except ValueError as e:
            print("Exception parsing 'col': ", e)
        try:
            row = int(input_string[sep_pos+1:sep_value])
        except ValueError as e:
            print("Exception parsing 'row': ", e)
        try:
            value = int(input_string[sep_value+1:])
        except ValueError as e:
            print("Exception parsing 'value': ", e)
        pixel_index = 0
        try:
            pixel_index = pmap.map(col=col, row=row)
        except IndexError as e:
            print("{}; col:'{:>3}' row:'{:>3}'".format(e, col, row))

        print(
            "pixel_index:'{:>3}' col:'{:>3}' row:'{:>3}'"
            "".format(pixel_index, col, row)
        )
        pixels.set_pixel_16bit_value(pixel_index, value, value, value)
        pixels.show()

    def check_input(self):
        """Check Input."""
        new_value = input()
        if "p" in new_value:
            self.handle_pixel_set(new_value)
        if "m" in new_value:
            self.handle_pixel_map_set(new_value)
        if "a" in new_value:
            self.animation_run = not self.animation_run
        # prepare new input
        # print("enter new values:")
        print(">>", end="")

    def run_test(self):
        """Test Main."""
        pmap.print_mapping()

        pixels.set_pixel_all_16bit_value(1, 1, 1)
        pixels.show()

        self.test_set_corners_to_colors()
        wait_with_print(3)
        self.test_set_2d_colors()
        wait_with_print(3)

        print(42 * '*')
        print("loop")
        if supervisor.runtime.serial_connected:
            print(
                "you can set a single pixel manually:\n"
                "example: 'p18:500' or 'm2,5:500'"
            )
        while True:
            if supervisor.runtime.serial_bytes_available:
                self.check_input()
            if self.animation_run:
                self.test_loop_2d_colors()


animation_helper = AnimationHelper()

##########################################
# main loop

if __name__ == '__main__':
    animation_helper.run_test()
