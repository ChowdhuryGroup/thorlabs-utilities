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

shutter.setShutterClose()

mot1 = mg.motor()
mot1.comset(1)
mot1.unpark(1)

rasterLength = 3000 #length of each raster unit - microns
speed = 2000 # speed in um/s (max is 2500 um/s)
rasterTime = rasterLength/speed #time seconds to make each raster
print(f"The raster time is: {rasterTime}")
numberRasters = 1 #number of rasters in the row
direction = 1 #moving right or left +/-1


if speed >= 2500:
    raise ValueError("Slow down there hoss (you're setting the speed too high)")
mot1.setspeed(1,speed)
shutter.setShutterOpen() #open shutter
mot1.move(1,rasterLength*direction) #move
shutter.setShutterClose() #close shutter
#move a little more and repeat
mot1.park(1)
