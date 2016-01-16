#!/usr/bin/env python
#
# Copyright 2016 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cwiid
from time import sleep
from datetime import datetime
from tspapi import API

class Driver(object):

    def __init__(self):
        self.wm = None
        self.api = API()
        self.button_delay = 0.01
        self._position = 0

    def send_measurement(self, metric_id, value, source, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime('%s')
        timestamp = int(timestamp)
        self.api.measurement_create(metric_id, value, source, timestamp)

    def connect(self, retries=10):
        """
        Attempt to connect to the Wiimote
        :param retries:
        :return:
        """
        print('Press 1+2 on your Wiimote now...')
        i = 1
        while self.wm is None:
            try:
                self.wm = cwiid.Wiimote()
            except RuntimeError:
                if i > retries:
                    quit()
            print(format("Error opening wiimote connection, attempt: {0}", str(i)))
            i += 1
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR | cwiid.RPT_STATUS

    def dispatch(self, buttons):

        if buttons & cwiid.BTN_LEFT:
            self.button_left()

        if buttons & cwiid.BTN_LEFT:
            self.button_left()

        if buttons & cwiid.BTN_RIGHT:
            self.button_right()

        if buttons & cwiid.BTN_UP:
            self.button_up()

        if buttons & cwiid.BTN_DOWN:
            self.button_down()

        if buttons & cwiid.BTN_1:
            self.button_1()

        if buttons & cwiid.BTN_2:
            self.button_2()

        if buttons & cwiid.BTN_A:
            self.button_a()

        if buttons & cwiid.BTN_B:
            self.button_b()

        if buttons & cwiid.BTN_HOME:
            self.button_home()

        if buttons & cwiid.BTN_MINUS:
            self.button_minus()

        if buttons & cwiid.BTN_PLUS:
            self.button_plus()

    def loop(self):
        while True:
            buttons = self.wm.state['buttons']
	    #print(self.wm.state['acc'])
            self.dispatch(buttons)
	    #sleep(0.25)
	    acc = self.wm.state['acc']
            self.send_measurement('WIIMOTE_ACC_X', acc[0], 'X')
            self.send_measurement('WIIMOTE_ACC_Y', acc[1], 'Y')
            self.send_measurement('WIIMOTE_ACC_Z', acc[2], 'Z')
	    #self.send_measurement('WIIMOTE_PILOT_POSITION', self._position, 'position');
	    self.send_measurement('WIIMOTE_ACCELEROMETER', acc[0], 'X');
	    self.send_measurement('WIIMOTE_ACCELEROMETER', acc[1], 'Y');
	    self.send_measurement('WIIMOTE_ACCELEROMETER', acc[2], 'Z');

    def message_loop(self):
	while True:
           sleep(0.01)
           messages = self.wm.get_mesg()   
           for msg in messages:
               if mesg[0] == cwiid.MESG_ACC: # If a accelerometer message
                   print(msg[1][cwiid.X])
                   print(msg[1][cwiid.Y])
                   print(msg[1][cwiid.Z])
               elif msg[0] == cwiid.MESG_BTN:
                   print(wiimote.state)

    def button_left(self):
        print('Left pressed')
        sleep(self.button_delay)

    def button_right(self):
        print('Right pressed')
        sleep(self.button_delay)

    def button_up(self):
        print('Up pressed')
        self._position += 1
        #sleep(self.button_delay)

    def button_down(self):
        print('Down pressed')
        self._position -= 1
        #sleep(self.button_delay)

    def button_1(self):
        print('Button 1 pressed')
        sleep(self.button_delay)

    def button_2(self):
        print('Button 2 pressed')
        sleep(self.button_delay)

    def button_a(self):
        print('Button A pressed')
	self.send_measurement('WIIMOTE_BUTTON_A', 1, 'ButtonA');

    def button_b(self):
        print('Button B pressed')
        sleep(self.button_delay)

    def button_home(self):
        print('Home Button pressed')
        sleep(self.button_delay)

    def button_minus(self):
        print('Minus Button pressed')
        sleep(self.button_delay)

    def button_plus(self):
        print('Plus Button pressed')
        sleep(self.button_delay)

    def run(self):
        self.connect()
        self.loop()


if __name__ == '__main__':
    d = Driver()
    d.run()
