#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import csv
import sys
from sense_hat import SenseHat
from time import strftime

sense = SenseHat()

sense.low_light = True

# Define the colours
r = (180, 0, 0)     # red
o = (255, 128, 0)   # orange
y = (170, 176, 0)   # yellow
g = (0, 255, 0)     # green
c = (0, 255, 255)   # cyan
b = (0, 0, 255)     # blue
p = (255, 0, 255)   # purple
n = (255, 128, 128) # pink
w =(255, 255, 255)  # white
k = (0, 0, 0)       # blank

rainbow = [r, o, y, g, c, b, p, n]

try:
    os.chdir('/home/pi/myNAS/env/')
except:
    for cycle in range(10):
        sense.clear(b)
        time.sleep(.25)
        sense.clear(r)
        time.sleep(.25)
    sense.show_letter("F", b, r)
    sys.exit()

while True:
    sense.clear()
    hour = time.strftime('%H')
    nap = hour >= '08' and hour < '20'
    
    if nap:
        for i in range(8):
            colour = rainbow[i]
            for x in range(8):
                sense.set_pixel(x, i, colour)
        time.sleep(1)
    if not nap:
        time.sleep(1)

    # Take readings from all three sensors
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    # Round the values to one decimal place
    t = round(t, 1)
    p = round(p, 1)
    h = round(h, 1)
  
    f = (t * 1.8) + 32
    f = round(f, 1)
  
    # Create the message
    message = "Temp: " + str(f) + " Pressure: " + str(p) + " Humidity: " + str(h)
  
    try:
        if t > 18.3 and t < 26.7:
          bg = g
        elif f >= 100:
          bg = r
        else:
          bg = y
        if nap:
            sense.show_message(message, scroll_speed=0.05, back_colour=bg)
        else:
            sense.clear()
            sense.set_pixel(0, 7, w)
            time.sleep(.1)
            sense.set_pixel(0, 7, bg)
            
    except TypeError as e:
        print(message)
        print(e)
        print('T: ' + str(f) + 'P: ' + str(p) + 'H: ' + str(h))
        sense.show_letter("E", b, r)
        sys.exit()
  
    c_date = str(time.strftime('%D'))
    c_d = str(time.strftime('%m-%d-%Y'))
    c_time = str(time.strftime('%H:%M:%S'))
    temp_data = [c_date, c_time, str(f), str(h), str(p)]
    repo = c_d + '-enviro.csv'
    print(temp_data)
    try:
        with open(repo, mode='a') as enviro:
            enviro_writer = csv.writer(enviro, delimiter=',', quotechar="'")
            enviro_writer.writerow(temp_data)
    except:
        for cycle in range(10):
            sense.clear(b)
            time.sleep(.25)
            sense.clear(r)
            time.sleep(.25)
        sense.show_letter("X", b, r)
        sys.exit()
    
    if nap:
        cd = 15
        for cycle in range(15):
            time.sleep(1)
            sense.show_message(str(cd), scroll_speed=0.02, back_colour=bg)
            cd -= 1
            time.sleep(1.5)
    if not nap:
        time.sleep(29)


