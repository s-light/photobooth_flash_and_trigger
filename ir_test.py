"""IR-Test."""

__doc__ = """
IR-Test.

IRLibCP by Chris Young

this test is based on
https://github.com/cyborg5/IRLibCP/blob/master/examples/decode_single.py
"""


import board
import IRLibProtocols
import IRLibDecodeBase
import IRLib_P01_NECd
import IRLib_P03_RC5d
import IRrecvPCI
# import IRLib.IRLibDecodeBase as IRLibDecodeBase
# import IRLib.IRLib_P01_NECd as IRLib_P01_NECd
# import IRLib.IRLib_P03_RC5d as IRLib_P03_RC5d
# import IRLib.IRrecvPCI as IRrecvPCI


##########################################
# helper

class MyDecodeClass(IRLibDecodeBase.IRLibDecodeBase):
    """Combined decoding for NEC and RC5."""

    def __init__(self):
        """init."""
        IRLibDecodeBase.IRLibDecodeBase.__init__(self)

    def decode(self):
        """Decode NEC and RC5."""
        if IRLib_P01_NECd.IRdecodeNEC.decode(self):
            return True
        elif IRLib_P03_RC5d.IRdecodeRC5.decode(self):
            return True
        return False


def revbits(x):
    """Reverse bit order."""
    rev = 0
    while x:
        rev <<= 1
        rev += x & 1
        x >>= 1
    return rev


##########################################
# function

def print_decoded_info(decoder):
    """Print information."""
    # 0b00000000111111110000100111110110
    # 0b00000000000000001111111111111000
    value_filtered = 0b1111111111111 & (decoder.value >> 3)
    value_short = 0xFFFF & decoder.value
    value_p1 = 0xFF & value_short
    value_p2 = 0xFF & (value_short >> 8)
    # value_p1 = 0b01111111 & (value_short << 1)
    # value_p2 = 0b01111111 & (value_short >> 8)
    value_rev = revbits(value_short)
    value_p1_rev = revbits(value_p1)
    value_p2_rev = revbits(value_p2)
    print(
        "{protocol:> 3}: "
        # "{value:0>8X} "
        # "'{value:0>32b}' "
        "'{value_filtered:0>14b}' "
        # "{value_short:0>4X} "
        # "'{value_short:0>16b}' "
        # "{value_p1:0>2X} "
        # "'{value_p1:0>8b}' "
        # "{value_p2:0>2X} "
        # "'{value_p2:0>8b}' "
        # "{value_p1_rev:0>2X} "
        # "'{value_p1_rev:0>8b}' "
        # "{value_p2_rev:0>2X} "
        # "'{value_p2_rev:0>8b}' "
        # "{value_rev:0>4X} "
        # "'{value_rev:0>16b}' "
        "".format(
            protocol=IRLibProtocols.Pnames[decoder.protocolNum],
            value=decoder.value,
            value_filtered=value_filtered,
            value_short=value_short,
            value_p1=value_p1,
            value_p2=value_p2,
            value_rev=value_rev,
            value_p1_rev=value_p1_rev,
            value_p2_rev=value_p2_rev,
        )
    )


def print_decoded_keymap(decoder):
    """Print information."""
    # 0b00000000111111110000100111110110
    # 0b00000000000000001111111111111000
    # 0b00000000000000001111100000000000
    value_filtered = 0b1111111111111 & (decoder.value >> 3)
    value_row = revbits(0b1111 & value_filtered)
    value_col = revbits(0b111 & (value_filtered >> 3))
    value_filtered2 = value_filtered >> 8
    value_filtered3 = 0b11111 & (decoder.value >> 11)
    print(
        "{protocol:> 3}: "
        "'{value_filtered:0>13b}' "
        "   "
        "{value_filtered3:>3} "
        "{value_filtered2:>3} "
        "'{value_filtered2:0>5b}' "
        "   "
        "row: "
        "{value_row:>2} "
        "'{value_row:0>4b}' "
        "   "
        "col: "
        "{value_col:>2} "
        "'{value_col:0>3b}' "
        "".format(
            protocol=IRLibProtocols.Pnames[decoder.protocolNum],
            value=decoder.value,
            value_filtered=value_filtered,
            value_filtered2=value_filtered2,
            value_filtered3=value_filtered3,
            value_row=value_row,
            value_col=value_col,
        )
    )


##########################################
# main
if __name__ == '__main__':
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    # print("\n")
    # animation.pixel_map_print_information()
    print("\n")
    print("\n")
    # animation.pixel_map_print_information()
    # print("\n")
    print(42 * '*')
    print("ir")
    myDecoder = MyDecodeClass()
    myReceiver = IRrecvPCI.IRrecvPCI(board.D7)
    myReceiver.enableIRIn()
    print("send a signal")
    while True:
        while (not myReceiver.getResults()):
            pass
        if myDecoder.decode():
            # print("success")
            # myDecoder.dumpResults(True)
            # print_decoded_info(myDecoder)
            print_decoded_keymap(myDecoder)
        myReceiver.enableIRIn()


##########################################
