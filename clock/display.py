"""This module helps to manage the attached e-Ink display"""
import logging
from lib.epd7in5_CYL import EPD

class Display:
    """
    This class provides a simple interface to the attached e-Ink display.
    """

    def __init__(self, connected=True):
        """Instantiates the Display class

        Args:
            connected (bool, optional): set to false to run without an attached screen.
                                        Defaults to True.
        """
        self._connected = connected
        self._sleeping = False
        if connected:
            self._epd = EPD()
        else:
            self._epd = type('obj', (object,), {
                'width' : 800,
                'height': 600
                })

    def init(self):
        """Initialises the display and clears the screen"""
        logging.info("Initialising display")
        if not self._connected:
            return
        self._epd.init()
        self._epd.clear()

    def size(self) -> tuple[int, int]:
        """Returns the size of the attached display, in pixels

        Returns:
            (int, int): Width and Height of the display in pixels
        """
        return self._epd.width, self._epd.height

    def middle(self) -> tuple[int, int]:
        """Returns the coordinates of the middle of the display, in pixels

        Returns:
            (int, int): X and Y coordinate of the middle of the display in pixels
        """
        return self._epd.width//2, self._epd.height//2

    def display(self, image):
        """Draws the provided image to the screen.

        Args:
            image (Any): The bitmap image data to send to the screen
        """
        if not self._connected:
            return
        if self._sleeping:
            self.init()
        self._epd.display(self._epd.getbuffer(image))

    def sleep(self):
        """Puts the screen into sleep mode without clearing it first"""
        logging.info("Putting display to sleep")
        if not self._connected:
            return
        self._epd.sleep()
        self._sleeping = True

    def stop(self):
        """Clears the display and turns it off"""
        logging.info("Shutting down display")
        if not self._connected:
            return
        self._epd.init()
        self._epd.clear()
        self._epd.sleep()
