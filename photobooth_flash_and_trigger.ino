/******************************************************************************

    photobooth_flash_and_trigger.ino
        simple remote trigger.
        debugout on usbserial interface: 115200baud

    hardware:
        Board:
            Arduino compatible (with serial port)
            LED on pin 9


    libraries used:
        ~ slight_DebugMenu
        ~ slight_ButtonInput
            written by stefan krueger (s-light),
                github@s-light.eu, http://s-light.eu, https://github.com/s-light/
            license: MIT

    written by stefan krueger (s-light),
        github@s-light.eu, http://s-light.eu, https://github.com/s-light/

******************************************************************************/
/******************************************************************************
    The MIT License (MIT)

    Copyright (c) 2019 Stefan Krüger

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
******************************************************************************/

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Includes
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// use "file.h" for files in same directory as .ino
// #include "file.h"
// use <file.h> for files in library directory
// #include <file.h>

#include "Keyboard.h"

#include <slight_DebugMenu.h>

#include <slight_ButtonInput.h>


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Info
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

void sketchinfo_print(Print &out) {
    out.println();
    //             "|~~~~~~~~~|~~~~~~~~~|~~~..~~~|~~~~~~~~~|~~~~~~~~~|"
    out.println(F("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"));
    out.println(F("|                       ^ ^                      |"));
    out.println(F("|                      (0,0)                     |"));
    out.println(F("|                      ( _ )                     |"));
    out.println(F("|                       \" \"                      |"));
    out.println(F("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"));
    out.println(F("| photobooth_flash_and_trigger.ino"));
    out.println(F("|   simple remote trigger."));
    out.println(F("|"));
    out.println(F("| This Sketch has a debug-menu:"));
    out.println(F("| send '?'+Return for help"));
    out.println(F("|"));
    out.println(F("| dream on & have fun :-)"));
    out.println(F("|"));
    out.println(F("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"));
    out.println(F("|"));
    //out.println(F("| compiled: Nov 11 2013  20:35:04"));
    out.print(F("| compiled: "));
    out.print(F(__DATE__));
    out.print(F("  "));
    out.print(F(__TIME__));
    out.println();
    out.print(F("| last changed: "));
    out.print(F(__TIMESTAMP__));
    out.println();
    //
    // out.println(F("|"));
    // out.print(F("| __FILE__: "));
    // out.print(F(__FILE__));
    // out.println();
    // out.print(F("| __BASE_FILE__"));
    // out.print(F(__BASE_FILE__));
    // out.println();
    // out.println(F("|"));
    //
    out.println(F("|"));
    out.println(F("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"));
    out.println();

    // __DATE__ Nov 11 2013
    // __TIME__ 20:35:04
    // __TIMESTAMP__ Tue Dec 27 14:14:04 2016
    // __FILE__  /home/stefan/mydata/arduino_sketchbook/libraries/slight_TLC5957/examples/src_arduino/photobooth_flash_and_trigger.ino
    // __BASE_FILE__ /tmp/arduino_build_330237/sketch/photobooth_flash_and_trigger.ino.cpp

}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// definitions (global)
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Debug Output

boolean infoled_state = 0;
const byte infoled_pin = A2;
const byte readyled_pin = A1;

uint32_t debugOut_LastAction = 0;
const uint16_t debugOut_interval = 1000; //ms

boolean debugOut_Serial_Enabled = 1;
boolean debugOut_LED_Enabled = 0;

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Menu

// slight_DebugMenu(Stream &in_ref, Print &out_ref, uint8_t input_length_new);
slight_DebugMenu myDebugMenu(Serial, Serial, 20);

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// button

const uint8_t remote_trigger_pin = A0;
const uint16_t remote_trigger_treshold = 700;

// slight_ButtonInput mybutton;
slight_ButtonInput mybutton_remote_trigger = slight_ButtonInput(
    // byte cbID_New
    1,
    // byte cbPin_New,
    remote_trigger_pin,
    // tCbfuncGetInput cbfuncGetInput_New,
    // button_getinput,
    button_getinput_remote,
    // tcbfOnEvent cbfCallbackOnEvent_New,
    button_event,
    // const uint16_t cwDuration_Debounce_New = 30,
      30,
    // const uint16_t cwDuration_HoldingDown_New = 1000,
    1000,
    // const uint16_t cwDuration_ClickSingle_New =   50,
      50,
    // const uint16_t cwDuration_ClickLong_New =   3000,
    3000,
    // const uint16_t cwDuration_ClickDouble_New = 1000
     500
);
slight_ButtonInput mybutton2 = slight_ButtonInput(
    // byte cbID_New
    2,
    // byte cbPin_New,
    A0,
    // tCbfuncGetInput cbfuncGetInput_New,
    button_getinput,
    // tcbfOnEvent cbfCallbackOnEvent_New,
    button_event,
    // const uint16_t cwDuration_Debounce_New = 30,
      30,
    // const uint16_t cwDuration_HoldingDown_New = 1000,
    1000,
    // const uint16_t cwDuration_ClickSingle_New =   50,
      50,
    // const uint16_t cwDuration_ClickLong_New =   3000,
    3000,
    // const uint16_t cwDuration_ClickDouble_New = 1000
     500
);

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// others

boolean send_keystroke = true;

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// functions
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// debug things

void debugOut_update() {
    uint32_t duration_temp = millis() - debugOut_LastAction;
    if (duration_temp > debugOut_interval) {
        debugOut_LastAction = millis();

        // const uint16_t raw = analogRead(mybutton_remote_trigger.pin);
        const uint16_t raw = analogRead(remote_trigger_pin);
        Serial.print(F("raw: "));
        Serial.print(raw);
        Serial.println();

        if ( debugOut_Serial_Enabled ) {
            Serial.print(millis());
            Serial.print(F("ms;"));
            Serial.println();
        }

        if ( debugOut_LED_Enabled ) {
            infoled_state = ! infoled_state;
            if (infoled_state) {
                //set LED to HIGH
                digitalWrite(infoled_pin, HIGH);
            } else {
                //set LED to LOW
                digitalWrite(infoled_pin, LOW);
            }
        }

    }
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Menu System

void menu__print_help(Print &out) {
    // help
    out.println(F("____________________________________________________________"));
    out.println();
    out.println(F("Help for Commands:"));
    out.println();
    out.println(F("\t '?': this help"));
    out.println(F("\t '!': sketch info"));
    out.println(F("\t 'y': toggle DebugOut livesign print"));
    out.println(F("\t 'Y': toggle DebugOut livesign LED"));
    out.println(F("\t 'x': tests"));
    out.println();
    out.print(F("\t 'r': toggle readyled 'r' ("));
    out.print(digitalRead(readyled_pin));
    out.println(F(")"));
    out.print(F("\t 'i': toggle infoled 'i' ("));
    out.print(digitalRead(infoled_pin));
    out.println(F(")"));
    out.print(F("\t 'k': toggle send_keystroke 'k' ("));
    out.print(send_keystroke);
    out.println(F(")"));
    // out.println();
    out.println(F("____________________________________________________________"));
}


// Main Menu
void handleMenu_Main(slight_DebugMenu *pInstance) {
    Print &out = pInstance->get_stream_out_ref();
    char *command = pInstance->get_command_current_pointer();
    // out.print("command: '");
    // out.print(command);
    // out.println("'");
    switch (command[0]) {
        // case 'h':
        // case 'H':
        case '?': {
            menu__print_help(out);
        } break;
        case '!': {
            sketchinfo_print(out);
        } break;
        case 'y': {
            out.println(F("\t toggle DebugOut livesign Serial:"));
            debugOut_Serial_Enabled = !debugOut_Serial_Enabled;
            out.print(F("\t debugOut_Serial_Enabled:"));
            out.println(debugOut_Serial_Enabled);
        } break;
        case 'Y': {
            out.println(F("\t toggle DebugOut livesign LED:"));
            debugOut_LED_Enabled = !debugOut_LED_Enabled;
            out.print(F("\t debugOut_LED_Enabled:"));
            out.println(debugOut_LED_Enabled);
        } break;
        case 'x': {
            // get state
            out.println(F("__________"));
            out.println(F("Tests:"));
            out.println(F("nothing to do."));
            out.println(F("__________"));
        } break;
        // ---------------------
        case 'r': {
            out.println(F("toggle readyled"));
            digitalWrite(readyled_pin, !digitalRead(readyled_pin));
        } break;
        case 'i': {
            out.println(F("toggle infoled"));
            digitalWrite(infoled_pin, !digitalRead(infoled_pin));
        } break;
        case 'k': {
            out.println(F("toggle send_keystroke"));
            send_keystroke = !send_keystroke;
        } break;
        //---------------------------------------------------------------------
        default: {
            if(strlen(command) > 0) {
                out.print(F("command '"));
                out.print(command);
                out.println(F("' not recognized. try again."));
            }
            pInstance->get_command_input_pointer()[0] = '?';
            pInstance->set_flag_EOC(true);
        }
    } // end switch

    // end Command Parser
}



//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// button

void button_init(Stream &out) {
    out.println(F("setup button input:"));

    out.println(F("  set pinMode INPUT_PULLUP"));
    // pinMode(mybutton_remote_trigger.getPin(), INPUT_PULLUP);
    pinMode(mybutton_remote_trigger.getPin(), INPUT);
    // ^ for this we have an external pullup..
    pinMode(mybutton2.getPin(), INPUT_PULLUP);
    // out.println(F("  setup port for Olimexino_32U4 HWB"));
	// DDRE &= B11111011;

    out.println(F("  begin()"));
    mybutton_remote_trigger.begin();
    mybutton2.begin();

    out.println(F("  finished."));
}

bool button_getinput_remote(byte id, byte pin) {
    // read input invert reading - button closes to GND.
    const uint8_t backup = digitalRead(readyled_pin);
    digitalWrite(readyled_pin, LOW);
    // const boolean state = !digitalRead(pin);
    const uint16_t raw = analogRead(pin);
    boolean state = false;
    if (raw > remote_trigger_treshold) {
        state = true;
    }
    digitalWrite(readyled_pin, backup);
    return state;
    // return (PINE & B00000100) != 0;
}

bool button_getinput(byte id, byte pin) {
    // read input invert reading - button closes to GND.
    return !digitalRead(pin);
    // return (PINE & B00000100) != 0;
}

void button_event(slight_ButtonInput *instance, byte event) {
    Stream &out = Serial;
    // out.print(F("Instance ID:"));
    // out.print((*instance).getID());
    // out.print(F(" "));
    // out.println();
    // out.print(F("Event: "));
    // (*instance).printEvent(out, event);
    // out.println();

    // show event additional infos:
    switch (event) {
        // case slight_ButtonInput::event_statechanged : {
        //     out.print(F("\t state: "));
        //     (*instance).printState(Serial);
        //     out.println();
        // } break;
        // click
        // case slight_ButtonInput::event_down : {
        //     out.print(F("the button is pressed down! do something.."));
        // } break;
        // case slight_ButtonInput::event_holddown : {
        //     out.print(F("duration active: "));
        //     out.println((*instance).getDurationActive());
        // } break;
        // case slight_ButtonInput::event_up : {
        //     out.print(F("up"));
        // } break;
        case slight_ButtonInput::event_click : {
            // out.println(F("click"));
            if ((*instance).getID() == mybutton_remote_trigger.getID()) {
                out.println(F("~~~42~~~ trigger!"));
                if (send_keystroke) {
                    Keyboard.write('s');
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                    delay(250);
                    digitalWrite(readyled_pin, HIGH);
                    delay(250);
                    digitalWrite(readyled_pin, LOW);
                }
            }
        } break;
        case slight_ButtonInput::event_click_long : {
            // out.println(F("click long"));
        } break;
        // case slight_ButtonInput::event_click_double : {
        //     // out.println(F("click double"));
        // } break;
        // case slight_ButtonInput::event_click_triple : {
        //     out.println(F("click triple"));
        // } break;
        case slight_ButtonInput::event_click_multi : {
            // out.print(F("click count: "));
            // out.println((*instance).getClickCount());
        } break;
    }  // end switch
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// sensor


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// setup
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void setup() {
    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // initialise PINs

        //LiveSign
        pinMode(infoled_pin, OUTPUT);
        digitalWrite(infoled_pin, LOW);
        pinMode(readyled_pin, OUTPUT);
        digitalWrite(readyled_pin, LOW);

        // as of arduino 1.0.1 you can use INPUT_PULLUP

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // initialise serial

        // wait for arduino IDE to release all serial ports after upload.
        delay(1000);
        // initialise serial
        Serial.begin(115200);

        // Wait for Serial Connection to be Opend from Host or
        // timeout after 6second
        uint32_t timeStamp_Start = millis();
        while( (! Serial) && ( (millis() - timeStamp_Start) < 2000 ) ) {
            // nothing to do
        }

        Serial.println();
        Serial.println();

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // print welcome

        sketchinfo_print(Serial);

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // setup sub-Parts

        Keyboard.begin();
        button_init(Serial);

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // show serial commands

        myDebugMenu.set_callback(handleMenu_Main);
        myDebugMenu.begin(true);

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // go

        Serial.println(F("wait 1s."));
        delay(1000);
        Serial.println(F("Loop:"));

} /** setup **/

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// main loop
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void loop() {
    myDebugMenu.update();
    mybutton_remote_trigger.update();
    mybutton2.update();
    debugOut_update();
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// THE END
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
