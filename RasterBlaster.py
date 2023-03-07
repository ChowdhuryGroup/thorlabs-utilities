# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 10:07:09 2021

@author: Conrad Kuz
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 18:44:22 2021

@author: Conrad Kuz
"""

import MellesGriot_nanomotionii as mg
import blitzer_shutter2 as shutter
import time
from playsound import playsound

shutter.setShutterClose()

mot1 = mg.motor()
mot1.comset(1)
mot1.unpark(1)
mot1.setspeed(1, 1000)

rasterLength = 3000 #length of each raster unit - microns?
rasterTime = 1 #time seconds to make each raster
numberRasters = 1 #number of rasters in the row
direction = -1 #moving right or left +/-1

speed = rasterLength/rasterTime #calculate speed
mot1.setspeed(1,speed)
shutter.setShutterOpen() #open shutter
mot1.move(1,rasterLength*direction) #move
shutter.setShutterClose() #close shutter
#move a little more and repeat
mot1.park(1)
