import time
import os
import pytest
from PIL import Image, ImageDraw, ImageFont
from display.epd_orig import EPD

input = os.path.join(os.path.abspath(os.getcwd()), "tests", "input")
output = os.path.join(os.path.abspath(os.getcwd()), "tests", "output")

def test_init():
    d = EPD()
    d.init()

def test_reset():
    d = EPD()
    d.reset()

def test_clear():
    d = EPD()
    d.clear()

def test_sleep():
    d = EPD()
    d.sleep()

def test_image():
    i = Image.open(os.path.join(input, "test_card.png"))
    d = EPD()
    d.init()
    d.display(d.getbuffer(i))
    d.sleep()

def test_rectangle():
    i = Image.open(os.path.join(input, "test_card.png"))
    d = EPD()
    d.init()
    d.display(d.getbuffer(i))
    time.sleep(5)
    c = ImageDraw.Draw(i)
    c.rounded_rectangle((100, 100, 700, 380), radius=30, fill=0)
    d.display(d.getbuffer(i))
    d.sleep()

# def test_partial():
#     i = Image.open(os.path.join(input, "test_card.png"))
#     d = EPD()
#     d.init()
#     # d.display(d.getbuffer(i))
#     # p = Image.new("1", (50, 50), color=0)

#     d.test_partial(d.getbuffer(i), (0, 0), (0, 0))
#     d.sleep()
