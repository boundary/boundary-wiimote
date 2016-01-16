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

    def queue_measurement(self, metric_id, value, source, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime('%s')
        timestamp = int(timestamp)
        self.api.measurement_create(metric_id, value, source, timestamp)
    def send_measurements(self):
        pass

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
                print("Error opening wiimote connection, attempt: {0}".format(str(i)))
                i += 1
                if i > retries:
                    quit()
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_STATUS
        print("connected!")

    def collect_battery_status(self):
	battery = float(self.wm.state['battery'])/100.0
        self.queue_measurement('WIIMOTE_BATTERY_STATUS', battery, 'Battery')

    def collect_button_status(self):

        buttons = self.wm.state['buttons']

        self.queue_measurement('WIIMOTE_BUTTON_LEFT', 1 if buttons & cwiid.BTN_LEFT else 0, 'ButtonLeft')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_UP else 0, 'ButtonLeft')

        self.queue_measurement('WIIMOTE_BUTTON_RIGHT', 1 if buttons & cwiid.BTN_RIGHT else 0, 'ButtonRight')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_RIGHT else 0, 'ButtonRight')

        self.queue_measurement('WIIMOTE_BUTTON_UP', 1 if buttons & cwiid.BTN_UP else 0, 'ButtonUp')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_UP else 0, 'ButtonUp')

        self.queue_measurement('WIIMOTE_BUTTON_DOWN', 1 if buttons & cwiid.BTN_DOWN else 0, 'ButtonDown')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_1 else 0, 'ButtonDown')

        self.queue_measurement('WIIMOTE_BUTTON_1', 1 if buttons & cwiid.BTN_1 else 0, 'Button1')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_1 else 0, 'Button1')

        self.queue_measurement('WIIMOTE_BUTTON_2', 1 if buttons & cwiid.BTN_2 else 0, 'Button2')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_2 else 0, 'Button2')

        self.queue_measurement('WIIMOTE_BUTTON_A', 1 if buttons & cwiid.BTN_A else 0, 'ButtonA')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_A else 0, 'ButtonA')

        self.queue_measurement('WIIMOTE_BUTTON_B', 1 if buttons & cwiid.BTN_B else 0, 'ButtonB')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_B else 0, 'ButtonB')

        self.queue_measurement('WIIMOTE_BUTTON_HOME', 1 if buttons & cwiid.BTN_HOME else 0, 'ButtonHome')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_HOME else 0, 'ButtonHome')

        self.queue_measurement('WIIMOTE_BUTTON_MINUS', 1 if buttons & cwiid.BTN_MINUS else 0, 'ButtonMinus')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_MINUS else 0, 'ButtonMinus')

        self.queue_measurement('WIIMOTE_BUTTON_PLUS', 1 if buttons & cwiid.BTN_PLUS else 0, 'ButtonPlus')
        self.queue_measurement('WIIMOTE_BUTTON', 1 if buttons & cwiid.BTN_PLUS else 0, 'ButtonPlus')

    def collect_accelerator_status(self):
	acc = self.wm.state['acc']
        self.queue_measurement('WIIMOTE_ACC_X', acc[0], 'X')
        self.queue_measurement('WIIMOTE_ACC_Y', acc[1], 'Y')
        self.queue_measurement('WIIMOTE_ACC_Z', acc[2], 'Z')
	self.queue_measurement('WIIMOTE_ACCELEROMETER', acc[0], 'X');
	self.queue_measurement('WIIMOTE_ACCELEROMETER', acc[1], 'Y');
	self.queue_measurement('WIIMOTE_ACCELEROMETER', acc[2], 'Z');

    def loop(self):
        while True:
            self.collect_battery_status()
            self.collect_button_status()
            self.collect_accelerator_status()

    def run(self):
        self.connect()
        self.loop()


if __name__ == '__main__':
    d = Driver()
    d.run()
