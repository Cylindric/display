#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import logging
import os
import sched
import sys
import time
import traceback
from Display import Display
from Canvas import Canvas

logging.basicConfig(level=logging.INFO)

def hourName(hour) :
   if hour == 1 : return 'one'
   if hour == 2 : return 'two'
   if hour == 3 : return 'three'
   if hour == 4 : return 'four'
   if hour == 5 : return 'five'
   if hour == 6 : return 'six'
   if hour == 7 : return 'seven'
   if hour == 8 : return 'eight'
   if hour == 9 : return 'nine'
   if hour == 10 : return 'ten'
   if hour == 11 : return 'eleven'
   if hour == 12 : return 'twelve'
   if hour == 13 : return 'one'
   if hour == 14 : return 'two'
   if hour == 15 : return 'three'
   if hour == 16 : return 'four'
   if hour == 17 : return 'five'
   if hour == 18 : return 'six'
   if hour == 19 : return 'seven'
   if hour == 20 : return 'eight'
   if hour == 21 : return 'nine'
   if hour == 22 : return 'ten'
   if hour == 23 : return 'eleven'
   if hour == 0 : return 'spooky'
   return ''

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

def tick(s=None):
    global mode, c, d
    now = datetime.datetime.now()
    logging.info(f"Tick {now}")
    t = now.time()

    # What mode we're in depends on the time of day
    if (t >= datetime.time(17,0)) or (t <= datetime.time(7,0)):
        if mode != "vague": logging.info("Switching mode to Vague")
        mode = "vague"
    else:
        if mode != "realtime": logging.info("Switching mode to RealTime")
        mode = "realtime"

    # How often we re-draw depends on what mode we're in
    if mode == "vague":
        # Vague mode updates the screen every 15 minutes
        delta = datetime.timedelta(minutes=15)
        next_refresh = roundTime(now + delta, roundTo=15*60)
        logging.info(f"Next vague update is at {next_refresh}")
        s.enterabs(next_refresh.timestamp(), 1, tick, argument=(s,))

    if mode == "realtime":
        # Realtime mode updates the screen every minute
        delta = datetime.timedelta(minutes=1)
        next_refresh = roundTime(now + delta, roundTo=60)
    
        logging.info(f"Next realtime update is at {next_refresh}")
        s.enterabs(next_refresh.timestamp(), 1, tick, argument=(s,))

    if mode == "testing":
        # Testing mode updates the screen more frequently
        delta = datetime.timedelta(seconds=15)
        next_refresh = roundTime(now + delta, roundTo=15)
    
        logging.info(f"Next testing update is at {next_refresh}")
        s.enterabs(next_refresh.timestamp(), 1, tick, argument=(s,))

    logging.info(f"Updating display with current time {now}")
    c.blank()
    if mode == "vague":
        c.display_time(f"{hourName(now.hour)}something", d.middle(), style="scaled_text")
        d.display(c.get_image())
    if mode == "realtime":
        c.display_time(now.strftime("%H:%M"), d.middle(), style="scaled_text")
        d.display(c.get_image())
    if mode == "testing":
        c.display_time(f"{hourName(now.hour)}something", d.middle(), style="scaled_text")
        d.display(c.get_image())

# Setup the scheduler
mode = "realtime"
s = sched.scheduler(time.time, time.sleep)
d = Display()
c = Canvas(d.size(), "origin_tech", 300)
c.auto_flip = True
d.init()

tick(s)
s.run()
