import logging
from lib.epd7in5_CYL import EPD

class Display:
    """
    This class provides a simple interface to the attached e-Ink display.
    """

    def __init__(self):
        self._sleeping = False
        self._epd = EPD()

    def init(self):
        logging.info("Initialising display")
        self._epd.init()
        self._epd.clear()
    
    def size(self):
        return self._epd.width, self._epd.height

    def middle(self):
        return self._epd.width//2, self._epd.height//2

    def display(self, image):
        if self._sleeping:
            self.init()
        self._epd.display(self._epd.getbuffer(image))

    def sleep(self):
        logging.info("Putting display to sleep")
        self._epd.sleep()
        self._sleeping = True
    
    def stop(self):
        logging.info("Shutting down display")
        self._epd.init()
        self._epd.clear()
        self._epd.sleep()
