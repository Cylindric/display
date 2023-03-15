"""This module provides the overal control for the display"""
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from display.canvas import Canvas
from display.clock import Clock
from display.screen import Screen

logger = logging.getLogger(__name__)

class Dashboard:
    """Contols the physical display, dashboard and assembles the various elements"""

    def __init__(self, connected=True, screenshot_path=None):
        """Instantiates the Dashboard class

        Args:
            connected (bool, optional): set to false to run without an attached screen.
                                        Defaults to True.
        """
        self._sched = BackgroundScheduler()
        self._display = Screen(connected=connected)
        self._clock = Clock(self._display.size())
        self._screenshot_path = screenshot_path

    def start(self):
        """Starts the dashboard and initialise the display"""
        self._sched.start()
        self._sched.add_job(self.tick, 'interval', seconds=5, max_instances=1)
        self._clock.start()
        self._display.init()

    def stop(self):
        """Stops the dashboard and puts the display to sleep"""
        self._sched.shutdown(wait=True)
        self._clock.stop()
        self._display.stop()

    def get_clock_state(self):
        """Returns the current mode of the Clock module"""
        return self._clock.get_state()

    def tick(self):
        """Call to update the state of the dashboard"""
        render_required = False
        render_required = render_required or self._clock.tick()

        if render_required:
            # assemble a new image from the components
            canvas = Canvas(self._display.size())
            canvas.auto_flip = True
            canvas.paste(self._clock.get_canvas().get_image())

            self._display.display(canvas)
            if self._screenshot_path:
                canvas.screenshot(os.path.join(self._screenshot_path, "latest.png"))
