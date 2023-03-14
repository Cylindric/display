import datetime
import logging
import os
import sched
import sys
import time
import traceback
from DisplayController import Display
from CanvasController import Canvas

class Clock():
    mode = "realtime"
    s = None
    d = None
    c = None

    def __init__(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.d = Display()
        self.c = Canvas(self.d.size(), "origin_tech", 300)

    def hourName(self, hour) :
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

    def roundTime(self, dt=None, roundTo=60):
        """Round a datetime object to any time lapse in seconds
        dt : datetime.datetime object, default now.
        roundTo : Closest number of seconds to round to, default 1 minute.
        Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        """
        if dt == None : dt = datetime.datetime.now()
        seconds = (dt.replace(tzinfo=None) - dt.min).seconds
        rounding = (seconds+roundTo/2) // roundTo * roundTo
        return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

    def tick(self, s=None):
        now = datetime.datetime.now()
        logging.info(f"Tick {now}")
        t = now.time()

        # What mode we're in depends on the time of day
        if (t >= datetime.time(17,0)) or (t <= datetime.time(7,0)):
            if self.mode != "vague": logging.info("Switching mode to Vague")
            self.mode = "vague"
        else:
            if self.mode != "realtime": logging.info("Switching mode to RealTime")
            self.mode = "realtime"

        # How often we re-draw depends on what mode we're in
        if self.mode == "vague":
            # Vague mode updates the screen every 15 minutes
            delta = datetime.timedelta(minutes=15)
            next_refresh = self.roundTime(now + delta, roundTo=15*60)
            logging.info(f"Next vague update is at {next_refresh}")
            self.s.enterabs(next_refresh.timestamp(), 1, self.tick, argument=(s,))

        if self.mode == "realtime":
            # Realtime mode updates the screen every minute
            delta = datetime.timedelta(minutes=1)
            next_refresh = self.roundTime(now + delta, roundTo=60)
        
            logging.info(f"Next realtime update is at {next_refresh}")
            self.s.enterabs(next_refresh.timestamp(), 1, self.tick, argument=(s,))

        if self.mode == "testing":
            # Testing mode updates the screen more frequently
            delta = datetime.timedelta(seconds=15)
            next_refresh = self.roundTime(now + delta, roundTo=15)
        
            logging.info(f"Next testing update is at {next_refresh}")
            self.s.enterabs(next_refresh.timestamp(), 1, self.tick, argument=(s,))

        logging.info(f"Updating display with current time {now}")
        self.c.blank()
        if self.mode == "vague":
            self.c.display_time(f"{hourName(now.hour)}something", self.d.middle(), style="scaled_text")
            self.d.display(self.c.get_image())
        if self.mode == "realtime":
            self.c.display_time(now.strftime("%H:%M"), self.d.middle(), style="scaled_text")
            self.d.display(self.c.get_image())
        if self.mode == "testing":
            self.c.display_time(f"{hourName(now.hour)}something", self.d.middle(), style="scaled_text")
            self.d.display(self.c.get_image())
        self.c.screenshot("html/latest.jpg")

    def start(self):
        # Setup the scheduler
        self.c.auto_flip = True
        self.d.init()

        self.tick(self.s)
        self.s.run()
