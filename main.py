"""Photobooth Animated Flash and IR-Trigger."""

__doc__ = """
Photobooth Animated Flash and IR-Trigger.

some LEDBoard_4x4_16bit and a IR Receiver for a photobooth project..
"""

import time

import board

import adafruit_fancyled.adafruit_fancyled as fancyled
# import animation
import ir_helper


##########################################
print(
    "\n" +
    (42 * '*') + "\n" +
    __doc__ + "\n" +
    (42 * '*') + "\n" +
    "\n"
)

##########################################
# helper function


##########################################
# function

def key_handler(self, key_value, key_name):
    """Print basic information about received key."""
    print(
        "IR-KEY: "
        "{value:>2} "
        "{key_name} "
        "".format(
            value=key_value,
            key_name=key_name,
        )
    )


# Positional offset into color palette to get it to 'spin'
offset = 0


# def main_animation():
#     """Animation example."""
#     global offset
#     for i in range(animation.pixel_count):
#         # Load each pixel's color from the palette using an offset, run it
#         # through the gamma function, pack RGB value and assign to pixel.
#         color = fancyled.palette_lookup(
#             animation.palette, offset + i / animation.pixel_count)
#         color = fancyled.gamma_adjust(color, brightness=0.1)
#         animation.pixels[i] = color
#         animation.pixels.show()
#
#         offset += 0.01  # Bigger number = faster spin


##########################################
# main
if __name__ == '__main__':
    print(42 * '*')
    time.sleep(5)

    # print("\n")
    # animation.pixel_map_print_information()
    print("\n")
    # animation.pixel_map_fill()
    print("\n")
    # animation.pixel_map_print_information()
    # print("\n")

    myIRHelper = ir_helper.IRHelper(board.D7, key_handler)
    print(42 * '*')
    print("rainbow loop")
    while True:
        # main_animation()
        myIRHelper.check()
