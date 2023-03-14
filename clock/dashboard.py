"""This module provides the overal control for the display"""
from clock import Clock

class Dashboard:
    """Contols the physical display, dashboard and assembles the various elements"""

    def __init__(self, connected=True):
        """Instantiates the Dashboard class

        Args:
            connected (bool, optional): set to false to run without an attached screen.
                                        Defaults to True.
        """
        self._clock = Clock(connected=connected)

    def start(self):
        """Starts the dashboard and initialise the display"""
        self._clock.start()

    def stop(self):
        """Stops the dashboard and puts the display to sleep"""
        self._clock.stop()

    def get_clock_state(self):
        """Returns the current mode of the Clock module"""
        return self._clock.get_state()
