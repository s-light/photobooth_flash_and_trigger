"""Photobooth Animated Flash and IR-Trigger."""

__doc__ = """
Photobooth Animated Flash and IR-Trigger.

some LEDBoard_4x4_16bit and a IR Receiver for a photobooth project..
"""

import time

import board

import adafruit_fancyled.adafruit_fancyled as fancyled
import animation
# import animation_minimal as animation
import ir_helper


##########################################
if __name__ == '__main__':
    print()
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print()

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
    if key_value is ir_helper.KeyMap.UP:
        animation.value_high += 5000
    elif key_value is ir_helper.KeyMap.DOWN:
        animation.value_high -= 5000
    elif key_value is ir_helper.KeyMap.OFF:
        animation.value_high = 100
        animation.set_all_black()
        animation.pixels_show()
    elif key_value is ir_helper.KeyMap.ON:
        animation.value_high = 1000
        animation.flash_fade()
    elif key_value is ir_helper.KeyMap.FLASH:
        animation.value_high = 1000
        animation.flash()


##########################################
# main


myIRHelper = ir_helper.IRHelper(board.D7, key_handler)


def main_setup():
    """Setup."""
    print(42 * '*')
    # time.sleep(0.5)
    # animation.pmap.print_mapping()

    animation.pixels.set_pixel_all_16bit_value(1, 1, 1)
    # animation.pixels.set_pixel_all_16bit_value(100, 100, 100)
    # animation.pixels.show()
    # animation.wait_with_print(1)
    animation.pixels_init_BCData()
    animation.pixels.show()
    # animation.wait_with_print(1)


def main_loop():
    """Loop."""
    myIRHelper.check()
    animation.animation_helper.main_loop()
    myIRHelper.check()
    # time.sleep(0.1)


if __name__ == '__main__':
    # print(42 * '*')
    print("setup")
    main_setup()
    print(42 * '*')
    print("loop")
    while True:
        main_loop()
