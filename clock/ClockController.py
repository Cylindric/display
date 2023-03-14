import datetime
import logging
from DisplayController import Display
from CanvasController import Canvas
from apscheduler.schedulers.background import BackgroundScheduler

logging.getLogger('apscheduler').setLevel(logging.WARNING)

class Clock():

    def __init__(self):
        self._mode = "stopped"
        self._newsched = BackgroundScheduler()
        self._display = Display()
        self._canvas = Canvas(self._display.size(), "origin_tech", 300)
        self._last_update = datetime.datetime(1977, 4, 20)
        self._next_update = datetime.datetime(1977, 4, 20)

    def get_state(self):
        return self._mode

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

    def tick(self):
        now = datetime.datetime.now()
        logging.info(f"Tick {now}")
        t = now.time()

        # What mode we're in depends on the time of day
        if (t >= datetime.time(17,0)) or (t <= datetime.time(9,0)):
            if self._mode != "vague": logging.info("Switching mode to Vague")
            self._mode = "vague"
        else:
            if self._mode != "realtime": logging.info("Switching mode to RealTime")
            self._mode = "realtime"

        # If we're not due to do anthing, don't do anything
        if self._next_update > now:
            logging.debug(f"Nothing to do until {self._next_update}")
            return False

        # How often we re-draw depends on what mode we're in
        if self._mode == "vague":
            # Vague mode updates the screen every 15 minutes
            delta = datetime.timedelta(minutes=15)
            self._next_update = self.roundTime(now + delta, roundTo=15*60)

        if self._mode == "realtime":
            # Realtime mode updates the screen every minute
            delta = datetime.timedelta(minutes=1)
            self._next_update = self.roundTime(now + delta, roundTo=60)

        if self._mode == "testing":
            # Testing mode updates the screen more frequently
            delta = datetime.timedelta(seconds=15)
            self._next_update = self.roundTime(now + delta, roundTo=15)

        logging.info(f"Next {self._mode} update is at {self._next_update}")

        logging.info(f"Updating display with current time {now}")
        self._canvas.blank()
        if self._mode == "vague":
            self._canvas.display_time(f"{self.hourName(now.hour)}something", self._display.middle(), style="scaled_text")
            self._display.display(self._canvas.get_image())
        if self._mode == "realtime":
            self._canvas.display_time(now.strftime("%H:%M"), self._display.middle(), style="scaled_text")
            self._display.display(self._canvas.get_image())
        if self._mode == "testing":
            self._canvas.display_time(f"{self.hourName(now.hour)}something", self._display.middle(), style="scaled_text")
            self._display.display(self._canvas.get_image())
        self._canvas.screenshot("public/img/latest.png")

        self._last_update = now

    def start(self):
        # Setup the scheduler
        self._mode = "starting"
        self._canvas.auto_flip = True
        self._display.init()
        self._newsched.start()
        self._newsched.add_job(self.tick, 'interval', seconds=5, max_instances=1)

    def stop(self):
        logging.info("Stopping Clock Controller...")
        self._newsched.shutdown(wait=True)
        self._display.stop()
        self._mode = "stopped"
        logging.info("Clock Controller stopped.")

