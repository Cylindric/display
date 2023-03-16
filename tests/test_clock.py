import datetime
import os
import pytest
from display.canvas import Canvas
from display.clock import Clock

output = os.path.join(os.path.abspath(os.getcwd()), "tests", "output")

def test_init():
    c = Clock((200,200))
    assert c.get_state() == "stopped"

def test_get_canvas_returns_image():
    c = Clock((200, 200))
    i = c.get_canvas()
    assert isinstance(i, Canvas)

def test_render_time_vaguely():
    c = Clock((200, 200))
    t = datetime.datetime(2023, 3, 15, 23, 49, 11, 232)
    c.render_time(t, "vague")
    c.get_canvas().screenshot(f"{output}/clock_test_render_time_vaguely.png")

def test_render_time_realtimely():
    c = Clock((200, 200))
    t = datetime.datetime(2023, 3, 15, 23, 49, 11, 232)
    c.render_time(t, "realtime")
    c.get_canvas().screenshot(f"{output}/clock_test_render_time_realtimely.png")
