"""IR-Helper."""

__doc__ = """
IR-Helper.

uses IRLibCP by Chris Young
https://github.com/cyborg5/IRLibCP
"""


import IRLibProtocols
import IRLibDecodeBase
import IRLib_P01_NECd
import IRLib_P03_RC5d
import IRrecvPCI


##########################################
# classes

class KeyMap(object):
    """Enum for Key - Value Mapping."""

    UP = 0
    DOWN = 16
    OFF = 8
    ON = 24

    RED = 4
    GREEN = 20
    BLUE = 12
    WHITE = 28

    FLASH = 26
    STROBE = 30
    FADE = 25
    SMOOTH = 29

    REDYELLOW1 = 2
    REDYELLOW2 = 6
    REDYELLOW3 = 1
    REDYELLOW4 = 5

    GREENTURQUOISE1 = 18
    GREENTURQUOISE2 = 22
    GREENTURQUOISE3 = 17
    GREENTURQUOISE4 = 21

    BLUEVIOLET1 = 10
    BLUEVIOLET2 = 14
    BLUEVIOLET3 = 9
    BLUEVIOLET4 = 13

    reverse_map = {
        0: "UP",
        16: "DOWN",
        8: "OFF",
        24: "ON",

        4: "RED",
        20: "GREEN",
        12: "BLUE",
        28: "WHITE",

        26: "FLASH",
        30: "STROBE",
        25: "FADE",
        29: "SMOOTH",

        2: "REDYELLOW1",
        6: "REDYELLOW2",
        1: "REDYELLOW3",
        5: "REDYELLOW4",

        18: "GREENTURQUOISE1",
        22: "GREENTURQUOISE2",
        17: "GREENTURQUOISE3",
        21: "GREENTURQUOISE4",

        10: "BLUEVIOLET1",
        14: "BLUEVIOLET2",
        9: "BLUEVIOLET3",
        13: "BLUEVIOLET4",
    }


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

    def decoded_key(self):
        """Decode key."""
        result = self.value
        if self.protocolNum == 1:
            result = 0b11111 & (self.value >> 11)
        return result

    def print_decoded_key(self):
        """Print information."""
        key_value = self.decoded_key()
        key_name = "UNKNOWN"
        if key_value in KeyMap.reverse_map:
            key_name = KeyMap.reverse_map[key_value]
        print(
            "{protocol:> 3}: "
            "{value:>2} "
            "{key_name} "
            "".format(
                protocol=IRLibProtocols.Pnames[self.protocolNum],
                value=key_value,
                key_name=key_name,
            )
        )


class IRHelper(object):
    """IR Helper Class."""

    def __init__(self, pin, key_handler_function=None):
        """init."""
        self.myDecoder = MyDecodeClass()
        self.myReceiver = IRrecvPCI.IRrecvPCI(pin)
        self.myReceiver.enableIRIn()

        # fallback to default
        self.key_handler_function = self._key_handler_function
        if key_handler_function:
            self.key_handler_function = key_handler_function

    def check(self):
        """Check."""
        if self.myReceiver.getResults():
            if self.myDecoder.decode():
                # self.myDecoder.print_decoded_key()
                key_value = self.myDecoder.decoded_key()
                key_name = "UNKNOWN"
                if key_value in KeyMap.reverse_map:
                    key_name = KeyMap.reverse_map[key_value]
                self.key_handler_function(self, key_value, key_name)
            self.myReceiver.enableIRIn()

    @staticmethod
    def _key_handler_function(self, key_value, key_name):
        """Map row and col to pixel_index."""
        self.myDecoder.print_decoded_key()


##########################################
# main
if __name__ == '__main__':
    import board
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    # print("\n")
    print("ir helper")
    myIRHelper = IRHelper(board.D7)
    while True:
        myIRHelper.check()


##########################################
