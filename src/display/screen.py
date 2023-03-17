"""This module helps to manage the attached e-Ink display"""
import logging
from PIL import Image
from display.epd_orig import EPD

class Screen:
    """
    This class provides a simple interface to the attached e-Ink display.
    """

    _bw_image_fix = False

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
            # Create a dummy display object, and slightly odd
            # size just to make it clear when testing that the
            # images came from a dummy screen
            self._epd = type('obj', (object,), {
                'width' : 1024,
                'height': 768
                })

    def init(self):
        """Initialises the display and clears the screen"""
        logging.info("Initialising display")
        if not self._connected:
            return
        self._epd.init()
        self._epd.clear()

    def clear(self):
        """Clears the screen"""
        logging.info("Clearing display")
        if not self._connected:
            return
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

        if self._bw_image_fix:
            image = self._fix_image_colours(image)

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

    def _fix_image_colours(self, image) -> Image:
        """Creates a new image where all pixels are either 0 or 1. 
        Any pixel with a colour value greater than 127 becomes 1."""

        newdata = []
        for colour in image.convert('1').getdata():
            if colour > 127:
                newdata.append(1)
            else:
                newdata.append(0)
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(newdata)
        return new_image
