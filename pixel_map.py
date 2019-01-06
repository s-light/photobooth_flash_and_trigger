"""Pixel Map."""

__doc__ = """
Pixel Map.

helper class to map 2D Pixel-Positions to internal Pixel-Orders.
"""


class PixelMap2D(object):
    """Helper Class to Map 2D Pixel things to 1D-Buffers."""

    def __init__(
            self,
            *, # noqa
            row_count=2,
            col_count=2,
            map_function=None,
            pixel_buffer=None):
        """."""
        super(PixelMap2D, self).__init__()
        self.row_count = row_count
        self.col_count = col_count
        self.pixel_count = self.row_count * self.col_count
        # default to internal map
        self.map_function = self._map_function
        if map_function:
            self.map_function = map_function
        self.pixel_buffer = pixel_buffer
        # prepare static map
        self.map_raw = [
            [0 for i in range(col_count)] for j in range(row_count)
        ]
        self.init_map()

    def init_map(self):
        """Prepare Static Map."""
        for row_index in range(self.row_count):
            for col_index in range(self.col_count):
                self.map_raw[row_index][col_index] = self.map_function(
                    self,
                    col=col_index,
                    row=row_index
                )

    def map(self, *, col=0, row=0):
        """Map row and col to pixel_index."""
        # print("map called.")
        # print("map_function: ", self.map_function)
        # pixel_index = self.map_function(self, col=col, row=row)
        # return pixel_index
        return self.map_raw[row][col]

    # @staticmethod
    def _map_function(self, *, col=0, row=0):
        """Map row and col to pixel_index."""
        pixel_index = (row * self.col_count) + col
        return pixel_index

    def print_mapping(self):
        """Print all Information we have."""
        max_length = str(len("{}".format(self.pixel_count)))
        format_string = (
            "Pixels & Mapping:\n"
            "  row_count      {row_count:>" + max_length + "}\n"
            "  col_count      {col_count:>" + max_length + "}\n"
            "  pixel_count    {pixel_count:>" + max_length + "}\n"
        )
        print(format_string.format(
            row_count=self.row_count,
            col_count=self.col_count,
            pixel_count=self.pixel_count,
        ))
        # print aligned 2d array
        value_format_string = "{:>" + max_length + "}, "
        print("[")
        for row_index in range(self.row_count):
            row_string = ""
            for col_index in range(self.col_count):
                row_string += value_format_string.format(
                    self.map(col=col_index, row=row_index)
                )
            print("    [" + row_string + "]")
        print("]")


##########################################
# main loop

def wait_with_print(duration=1):
    """Wait with print."""
    import time
    step_duration = 0.5
    waiting_duration = 0
    while waiting_duration < duration:
        # print(". ", end='', flush=True)
        print(".", end='')
        time.sleep(step_duration)
        waiting_duration += step_duration
    print("")


def test_main():
    """Test Main."""
    #####################
    # default map
    # pmap = PixelMap2D(row_count=4, col_count=4)
    # pmap.print_mapping()
    # wait_with_print(1)

    #####################
    # simple inverted map
    def mymap_inverse(self, row, col):
        """Map row and col to pixel_index."""
        # reverse
        # invert row and col
        row_inv = (self.row_count-1) - row
        col_inv = (self.col_count-1) - col
        pixel_index = (row_inv * self.col_count) + col_inv
        return pixel_index

    pmap = PixelMap2D(row_count=4, col_count=4, map_function=mymap_inverse)
    pmap.print_mapping()
    # wait_with_print(1)

    #####################
    # TLC5957 mapping
    def mymap_tlc5957_single(self, row, col):
        """Map row and col to pixel_index."""
        LEDBoard_row_count = 4
        LEDBoard_col_count = 4
        # CHIP_LED_COUNT = 16
        # split chip position from chip_inner
        chipin_row = row % LEDBoard_row_count
        chipin_col = col % LEDBoard_col_count
        # chip_row = row / LEDBoard_row_count
        # chip_col = col / LEDBoard_col_count

        chipin_row_inv = (LEDBoard_row_count - 1) - chipin_row
        chipin_col_inv = (LEDBoard_col_count - 1) - chipin_col
        chipin_pixel_index = (
            (chipin_row_inv * LEDBoard_col_count) + chipin_col_inv
        )

        pixel_index = chipin_pixel_index

        return pixel_index

    pmap = PixelMap2D(
        row_count=4,
        col_count=8,
        map_function=mymap_tlc5957_single)
    pmap.print_mapping()
    # wait_with_print(1)

    def mymap_tlc5957(self, row, col):
        """Map row and col to pixel_index."""
        # this version only works for Boards rows == 4

        LEDBoard_row_count = 4
        LEDBoard_col_count = 4
        CHIP_LED_COUNT = 16
        CHIP_COUNT = self.pixel_count // CHIP_LED_COUNT

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

        pixel_index = (chipin_pixel_index * CHIP_COUNT) + chip_col_inv

        return pixel_index

    pmap = PixelMap2D(row_count=4, col_count=8, map_function=mymap_tlc5957)
    pmap.print_mapping()
    wait_with_print(10)


if __name__ == '__main__':
    test_main()
