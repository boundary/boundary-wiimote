#!/usr/bin/env python
#
# Copyright 2015 BMC Software, Inc.
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
import time
# import i2c

#connecting to the Wiimote. This allows several attempts
# as first few often fail.
print 'Press 1+2 on your Wiimote now...'
wm = None
i=2
while not wm:
    try:
        wm=cwiid.Wiimote()
    except RuntimeError:
        if (i>10):
            quit()
            break
        print(format("Error opening wiimote connection, attempt: {0}", str(i)))
        i +=1

# set Wiimote to report button presses and accelerometer state
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

#turn on led to show connected
wm.led = 1
