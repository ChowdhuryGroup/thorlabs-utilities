# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 18:44:22 2021

@author: Conrad Kuz
"""

import MellesGriot_nanomotionii as mg
import blitzer_shutter2 as shutter
import time
from playsound import playsound


mot1 = mg.motor()
mot1.comset(1)
mot1.unpark(1)
mot1.setspeed(1, 1000)

long = False #False if short pulse(less than 900 milliseconds)
shutterLength = 2000  #long: seconds short: *0.1millisecond
delay = 5 #offset between trigger and shutter open
shots = 5  #number of shots
direction = -1 #+1 or -1 for left or right movement

for i in range(shots):
    mot1.move(1,100*direction)
    time.sleep(.25)
    if long == False:
        shutter.openShutter(shutterLength,delay)
    else:
        shutter.openShutterLong(shutterLength)
    time.sleep(.1)
    print(i+1)

playsound('ClownHorn.mp3')

time.sleep(5)
mot1.setspeed(1, 100)
mot1.move(1, shots*-100*direction )
mot1.park(1)


