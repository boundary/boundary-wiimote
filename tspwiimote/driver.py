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
from datetime import datetime
from tspapi import API
from tspapi import Measurement


class Driver(object):
    def __init__(self, email=None, api_token=None):
        self._wm = None
        self._api = API(email=email, api_token=api_token)
        self._buttons = None
        self._accelerometers = None
        self._measurements = None
        self._timestamp = None

    def queue_measurement(self, metric, value, source):
        self._measurements.append(Measurement(metric=metric, value=value, source=source, timestamp=self._timestamp)

    def send_measurements(self):
        self._api.measurement_create_batch(self._measurements)

    def connect(self, retries=10):
        """
        Attempt to connect to the Wiimote
        :param retries: Number of times to attempting connection before raising an exception.
        :return:
        """
        print('Press 1+2 on your Wiimote now...')
        i = 1
        while self._wm is None:
            try:
                self._wm = cwiid.Wiimote()
            except RuntimeError:
                print("Error opening wiimote connection, attempt: {0}".format(str(i)))
                i += 1
                if i > retries:
                    raise RuntimeError
        self._wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_STATUS
        print("connected!")

    def button_status(self, button):
        return 1 if self._buttons & button else 0

    def collect_init(self):
        # Initialze the array to hold the collected measurements
        self._measurements = []

        # Get the current time and use for all measurements
        self._timestamp = int(datetime.now().strftime('%s'))

        # Snapshot the current state of buttons and accelerometers
        self._buttons = self._wm.state['buttons']
        self._accelerometers = self._wm.state['acc']
        self._battery = self._wm.state['battery']

    def collect_battery_status(self):
        self.queue_measurement('WIIMOTE_BATTERY', float(self._battery)/100.0, 'battery')

    def collect_button_status(self):

        button_left = self.button_status(cwiid.BTN_LEFT)
        self.queue_measurement('WIIMOTE_BUTTON_LEFT', button_left, 'button-left')
        self.queue_measurement('WIIMOTE_BUTTON', button_left, 'button-left')

        button_right = self.button_status(cwiid.BTN_RIGHT)
        self.queue_measurement('WIIMOTE_BUTTON_RIGHT', button_right, 'button-right')
        self.queue_measurement('WIIMOTE_BUTTON', button_right, 'button-right')

        button_up = self.button_status(cwiid.BTN_UP)
        self.queue_measurement('WIIMOTE_BUTTON_UP', button_up, 'button-up')
        self.queue_measurement('WIIMOTE_BUTTON', button_up, 'button-up')

        button_down = self.button_status(cwiid.BTN_DOWN)
        self.queue_measurement('WIIMOTE_BUTTON_DOWN', button_down, 'button-down')
        self.queue_measurement('WIIMOTE_BUTTON', button_down, 'button-down')

        button_1 = self.button_status(cwiid.BTN_1)
        self.queue_measurement('WIIMOTE_BUTTON_1', button_1, 'button-1')
        self.queue_measurement('WIIMOTE_BUTTON', button_1, 'button-1')

        button_2 = self.button_status(cwiid.BTN_2)
        self.queue_measurement('WIIMOTE_BUTTON_2', button_2, 'button-2')
        self.queue_measurement('WIIMOTE_BUTTON', button_2, 'button-2')

        button_a = self.button_status(cwiid.BTN_A)
        self.queue_measurement('WIIMOTE_BUTTON_A', button_a, 'button-a')
        self.queue_measurement('WIIMOTE_BUTTON', button_a, 'button-a')

        button_b = self.button_status(cwiid.BTN_B)
        self.queue_measurement('WIIMOTE_BUTTON_B', button_b, 'button-b')
        self.queue_measurement('WIIMOTE_BUTTON', button_b, 'button-b')

        button_home = self.button_status(cwiid.BTN_HOME)
        self.queue_measurement('WIIMOTE_BUTTON_HOME', button_home, 'button-home')
        self.queue_measurement('WIIMOTE_BUTTON', button_home, 'button-home')

        button_minus = self.button_status(cwiid.BTN_MINUS)
        self.queue_measurement('WIIMOTE_BUTTON_MINUS', button_minus, 'button-minus')
        self.queue_measurement('WIIMOTE_BUTTON', button_minus, 'button-minus')

        button_plus = self.button_status(cwiid.BTN_PLUS)
        self.queue_measurement('WIIMOTE_BUTTON_PLUS', button_plus, 'button-plus')
        self.queue_measurement('WIIMOTE_BUTTON', button_plus, 'button-plus')

    def collect_accelerator_status(self):
        self.queue_measurement('WIIMOTE_ACCELEROMETER_X', self._accelerometers[0], 'accelerometer-x')
        self.queue_measurement('WIIMOTE_ACCELEROMETER_Y', self._accelerometers[1], 'accelerometer-y')
        self.queue_measurement('WIIMOTE_ACCELEROMETER_Z', self._accelerometers[2], 'accelerometer-z')
        self.queue_measurement('WIIMOTE_ACCELEROMETER', self._accelerometers[0], 'accelerometer-x');
        self.queue_measurement('WIIMOTE_ACCELEROMETER', self._accelerometers[1], 'accelerometer-y');
        self.queue_measurement('WIIMOTE_ACCELEROMETER', self._accelerometers[2], 'accelerometer-z');

    def collection_loop(self):
        while True:
            self.collect_init()
            self.collect_battery_status()
            self.collect_button_status()
            self.collect_accelerator_status()

    def run(self):
        self.connect()
        self.collection_loop()
