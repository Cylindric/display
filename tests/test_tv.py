import datetime
import os
import pytest
from display.canvas import Canvas
from display.tv import Tv

output = os.path.join(os.path.abspath(os.getcwd()), "tests", "output")

def test_init():
    tv = Tv((200,100))

def test_get_canvas_returns_image():
    tv = Tv((200,100))
    i = tv.get_canvas()
    assert isinstance(i, Canvas)

def test_render():
    tv = Tv((800,100))
    tv._calendar_data = [
        {
            'seriesId': 1,
            'seasonNumber': 2,
            'episodeNumber': 3,
            'title': 'Great Episode',
            'airDate': '2023-03-15',
            'series': {
                'title': 'Awesome series'
            }
        },
        {
            'seriesId': 2,
            'seasonNumber': 3,
            'episodeNumber': 4,
            'title': 'Okay Episode',
            'airDate': '2023-03-16',
            'series': {
                'title': 'Middling series'
            }
        }
    ]
    tv.render()
    tv.get_canvas().screenshot(f"{output}/tv_test_render.png")

# def test_render_time_vaguely():
#     tv = Tv((200,100))
#     t = datetime.datetime(2023, 3, 15, 23, 49, 11, 232)
#     c.render_time(t, "vague")
#     c.get_canvas().screenshot(f"{output}/clock_test_render_time_vaguely.png")

# def test_render_time_realtimely():
#     tv = Tv((200,100))
#     t = datetime.datetime(2023, 3, 15, 23, 49, 11, 232)
#     c.render_time(t, "realtime")
#     c.get_canvas().screenshot(f"{output}/clock_test_render_time_realtimely.png")
