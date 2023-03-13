#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from lib.epd7in5_CYL import EPD
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

BBOX_WIDTH = 2
BBOX_HEIGHT = 3
X = 0
Y = 1

fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

try:
    epd = EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()


    logging.info("Font Test...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    font_glossy = ImageFont.truetype(os.path.join(fontdir, "glossy.ttf"), 96)

    size_hello = font_glossy.getbbox("hello")
    size_space = font_glossy.getbbox(" ")
    size_world = font_glossy.getbbox("world")

    width = (size_hello[BBOX_WIDTH] + size_space[BBOX_WIDTH] + size_world[BBOX_WIDTH])
    height = (size_hello[BBOX_HEIGHT])

    middle = (epd.width/2, epd.height/2)

    cursor = (middle[X] - (width/2), middle[Y] - height/2)

    draw.text(cursor, 'hello', font = font_glossy, fill = 0)
    cursor = (cursor[X]+size_space[BBOX_WIDTH]+size_world[BBOX_WIDTH], cursor[Y])

    draw.text(cursor, 'world', font = font_glossy, fill = 0)

    # Rotate the image to put the connector at the top
    Himage = Himage.transpose(Image.ROTATE_180)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
