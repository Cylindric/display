"""This module help to manage the clock component"""
import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from display import Display
from canvas import Canvas

logging.getLogger('apscheduler').setLevel(logging.WARNING)

class Clock():
    """
    This class draws a variety of clocks depending on the time of day.
    """

    def __init__(self, connected=True):
        """Instantiates the Clock class

        Args:
            connected (bool, optional): set to false to run without an attached screen.
                                        Defaults to True.
        """
        self._mode = "stopped"
        self._newsched = BackgroundScheduler()
        self._display = Display(connected=connected)
        self._canvas = Canvas(self._display.size(), "origin_tech", 300)
        self._last_update = datetime.datetime(1977, 4, 20)
        self._next_update = datetime.datetime(1977, 4, 20)

    def get_state(self):
        """Returns the current state of the clock."""
        return self._mode

    # pylint: disable=multiple-statements
    def hour_name(self, hour):
        """Returns an English name for a particular hour of the day."""
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

    def round_time(self, date_time=None, round_to=60):
        """Round a datetime object to any time lapse in seconds
        date_time : datetime.datetime object, default now.
        round_to : Closest number of seconds to round to, default 1 minute.
        Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        """
        if date_time is None : date_time = datetime.datetime.now()
        seconds = (date_time.replace(tzinfo=None) - date_time.min).seconds
        rounding = (seconds+round_to/2) // round_to * round_to
        return date_time + datetime.timedelta(0,rounding-seconds,-date_time.microsecond)

    def tick(self):
        """Performs any actions required on this tick."""

        now = datetime.datetime.now()
        logging.info("Tick %s", now)
        t = now.time()

        # What mode we're in depends on the time of day
        if (t >= datetime.time(17,0)) or (t <= datetime.time(9,0)):
            if self._mode != "vague":
                logging.info("Switching mode to Vague")
            self._mode = "vague"
        else:
            if self._mode != "realtime":
                logging.info("Switching mode to RealTime")
            self._mode = "realtime"

        # If we're not due to do anthing, don't do anything
        if self._next_update > now:
            logging.debug("Nothing to do until %s", self._next_update)
            return False

        # How often we re-draw depends on what mode we're in
        if self._mode == "vague":
            # Vague mode updates the screen every 15 minutes
            delta = datetime.timedelta(minutes=15)
            self._next_update = self.round_time(now + delta, round_to=15*60)

        if self._mode == "realtime":
            # Realtime mode updates the screen every minute
            delta = datetime.timedelta(minutes=1)
            self._next_update = self.round_time(now + delta, round_to=60)

        logging.info("Updating display with current time %s", now)
        self._canvas.blank()
        if self._mode == "vague":

            self._canvas.display_time(
                f"{self.hour_name(now.hour)}something",
                self._display.middle(),
                style="scaled_text")

            self._display.display(self._canvas.get_image())

        if self._mode == "realtime":
            self._canvas.display_time(
                now.strftime("%H:%M"),
                self._display.middle(),
                style="scaled_text")

            self._display.display(self._canvas.get_image())

        self._canvas.screenshot("public/img/latest.png")
        self._last_update = now

        logging.info("Next %s update is at %s", self._mode, self._next_update)

    def start(self):
        """
        Starts the main Clock controller, and sets up the scheduler for updates.
        """

        self._mode = "starting"
        self._canvas.auto_flip = True
        self._display.init()
        self._newsched.start()
        self._newsched.add_job(self.tick, 'interval', seconds=5, max_instances=1)

    def stop(self):
        """
        Stops the main Clock controller, turns off the screen, and stops any pending schedules.
        """

        logging.info("Stopping Clock Controller...")
        self._newsched.shutdown(wait=True)
        self._display.stop()
        self._mode = "stopped"
        logging.info("Clock Controller stopped.")
