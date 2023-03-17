import time
import os
import pytest
from PIL import Image, ImageDraw
from display.screen import Screen

input = os.path.join(os.path.abspath(os.getcwd()), "tests", "input")
output = os.path.join(os.path.abspath(os.getcwd()), "tests", "output")

@pytest.mark.screen
def test_init():
    s = Screen()
    s.init()

@pytest.mark.screen
def test_clear():
    s = Screen()
    s.init()
    s.clear()

@pytest.mark.screen
def test_sleep():
    s = Screen()
    s.sleep()

def test_size():
    s = Screen(connected=False)
    size = s.size()
    assert size[0] == 1024
    assert size[1] == 768

def test_middle():
    s = Screen(connected=False)
    middle = s.middle()
    assert middle[0] == 512
    assert middle[1] == 384

@pytest.mark.screen
def test_screen_display():
    s = Screen()
    i = Image.open(os.path.join(input, "test_card.png"))
    i = i.convert('1')
    i.save(f"{output}/screen_display.png")
    s.init()
    s.display(i)
    time.sleep(5)
    s.sleep()