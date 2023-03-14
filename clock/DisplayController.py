import logging
from lib.epd7in5_CYL import EPD
from PIL import Image,ImageDraw,ImageFont

class Display:
    epd = None
    sleeping = False

    def __init__(self):
        self.epd = EPD()

    def init(self):
        self.epd.init()
        self.epd.Clear()
    
    def size(self):
        return self.epd.width, self.epd.height

    def middle(self):
        return self.epd.width//2, self.epd.height//2

    def display(self, image):
        if self.sleeping:
            self.init()
        self.epd.display(self.epd.getbuffer(image))

    def sleep(self):
        self.epd.sleep()
        self.sleeping = True