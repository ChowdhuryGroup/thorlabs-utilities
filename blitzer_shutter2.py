# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 09:57:19 2021

@author: Conrad Kuz
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
import time
from playsound import playsound

def openShutter(duration,delay):
    #requires trigger input in timing io
    #input as follow: duration units 20 = 2ms
    with nidaqmx.Task() as t:
        t.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        
        #set update time per second
        t.timing.cfg_samp_clk_timing(10000,sample_mode=AcquisitionType.FINITE,samps_per_chan=10000)
        #starts task on trigger
        t.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/PFI0",trigger_edge=Edge.RISING)
        
        delay=0
        shutter_time = int(duration)

        delay=int(delay)
        signallist = [0.0]*(1+delay)+[5.0]*shutter_time+[0.0]*(10000-shutter_time-delay-1)
        t.write(signallist)
        t.start()
        t.wait_until_done()
        t.stop()
        
def openShutterLong(duration):

    #for longer open times: duration in seconds
    with nidaqmx.Task() as t:
        t.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        t.write(5.0, auto_start=True)
        time.sleep(duration)
        t.write(0.0, auto_start=True)
        t.stop()

def setShutterOpen():
    with nidaqmx.Task() as t:
        t.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        t.write(5.0, auto_start=True)
        t.stop()
def setShutterClose():
    with nidaqmx.Task() as t:
        t.ao_channels.add_ao_voltage_chan('Dev1/ao0')
        t.write(0.0, auto_start=True)
        t.stop()

if __name__ == '__main__':
    if input("Long? (y/n): ") == "y":
        shutter_time = float(input("shutter time(seconds): "))
        user_input = input("enter to shoot, e to end: ")
        count = 1
        while user_input != "e":
            openShutterLong(shutter_time)
            print(count)
            if count < 20:
                count += 1
            else:
                playsound('ClownHorn.mp3')
                count = 1
            user_input = input("enter to shoot, e to end: ")
        
    else:
        shutter_time = int(input("shutter time (20=2ms):"))
        #delay = input("delay (20=2ms): ")
        delay = 5
        user_input = input("enter to shoot, e to end: ")
        while user_input != "e":
            delay = int(delay)
            openShutter(shutter_time,delay)
            user_input = input("enter to shoot, e to end: ")
            #delay = input("delay (20=2ms): ")