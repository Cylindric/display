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
frame = 0

# Just a dumb little helper to compare expected versus displayed images
def screenshot(i):
    global frame
    i.save("f{:03d}.jpg".format(frame))
    frame += 1

try:
    font_glossy = ImageFont.truetype(os.path.join(fontdir, "glossy.ttf"), 96)

    epd = EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()


    # Get some sizes of things so we can lay them out later
    size_hello = font_glossy.getbbox("hello")
    size_space = font_glossy.getbbox(" ")
    size_world = font_glossy.getbbox("world")
    size_total = ((size_hello[BBOX_WIDTH] + size_space[BBOX_WIDTH] + size_world[BBOX_WIDTH]), (size_hello[BBOX_HEIGHT]))

    logging.info(f"Hello: ${size_hello}.")
    logging.info(f"Space: ${size_space}.")
    logging.info(f"World: ${size_world}.")
    logging.info(f"Total: ${size_total}.")

    # Coordinates are (0,0) at the top-left
    screen_middle = (epd.width/2, epd.height/2)


    ###########################################################################
    # SCENE SETUP
    ###########################################################################
    # Create a new canvas
    Himage = Image.new('L', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    screenshot(Himage)

    ###########################################################################
    # FRAME 1
    ###########################################################################

    # Work out where the "cursor" position needs to be.
    # Text is drawn from the top-left pixel of the bounding box
    cursor = (screen_middle[X] - (size_total[X]/2), screen_middle[Y] - size_total[Y]/2)

    # Put the text on the canvas
    draw.text(cursor, 'hello', font = font_glossy, fill = 0)
    
    # Update the "cursor" to where the next character would be drawn after the previous word
    cursor = (cursor[X]+size_space[BBOX_WIDTH]+size_world[BBOX_WIDTH], cursor[Y])

    # Put more text on the canvas
    draw.text(cursor, 'world', font = font_glossy, fill = 0)

    # Send the image to the screen
    screenshot(Himage)
    epd.display(epd.getbuffer(Himage))

    # Sleep
    time.sleep(2)

    ###########################################################################
    # FRAME 2
    ###########################################################################
    # Blot out the word "World" with a blank rectangle
    blanker = [cursor, (cursor[X]+size_world[BBOX_WIDTH], cursor[Y]+size_world[BBOX_HEIGHT])]
    draw.rectangle(blanker, fill = 255)
    screenshot(Himage)

    # Draw a new word where "world" was before
    draw.text(cursor, 'everyone', font = font_glossy, fill = 0)
    screenshot(Himage)

    # Send the image to the screen
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)


    ###########################################################################
    # SCENE END
    ###########################################################################
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
