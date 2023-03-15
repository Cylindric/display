import os
import pytest
from PIL import Image, ImageDraw, ImageFont
from display.canvas import Canvas

output = os.path.join(os.path.abspath(os.getcwd()), "tests", "output")

def test_init():
    c = Canvas((200, 200))

def test_screenshot_handles_invalid_filename():
    c = Canvas((100, 100))
    with pytest.raises(RuntimeError, match=r"Invalid filename.*"):
        c.screenshot("filename_no_extension")

def test_screenshot_creates_file(tmp_path):
    c = Canvas((100, 100))
    path = tmp_path / "test.png"
    c.screenshot(str(path))

    assert len(list(tmp_path.iterdir())) == 1

    st_size = path.stat().st_size
    assert st_size == 312 # the expected size of a 100x100 blank PNG

def test_get_image_returns_image():
    c = Canvas((100, 100))
    i = c.get_image()
    assert isinstance(i, Image.Image)

def test_blank():
    c = Canvas((100, 100))
    c.blank()
    c.screenshot(f"{output}/canvas_blank.png")

def test_create_text_object_needs_valid_scale():
    c = Canvas((200, 200), font="origin_tech")
    with pytest.raises(ValueError, match=r"Invalid scale.*"):
        t = c.create_text_object("test")

def test_create_text_object_needs_one_scale():
    c = Canvas((200, 200), font="origin_tech")
    with pytest.raises(ValueError, match=r"Invalid scale.*"):
        t = c.create_text_object("test", width=100, height=100)

def test_draw_text():
    c = Canvas((200, 200), font="origin_tech")
    c.draw_text("Top Left", 150, anchor="top-left")
    c.screenshot(f"{output}/canvas_draw_text.png")

def test_draw_text_at_position():
    c = Canvas((200, 200), font="origin_tech")
    c.draw_text("top-middle", 150, position=(25,0), anchor="top-left")
    c.screenshot(f"{output}/canvas_draw_text_at_position.png")

def test_draw_text_at_position_baseline():
    c = Canvas((200, 200), font="origin_tech")
    c.draw_text("baseline", 150, position=(0,200))
    c.screenshot(f"{output}/canvas_draw_text_at_position_baseline.png")

def test_draw_text_centred_at_position():
    c = Canvas((200, 200), font="origin_tech")
    c.draw_text("centered", 200, position=(100,100), anchor="centre")
    c.screenshot(f"{output}/canvas_draw_text_centred_at_position.png")

def test_draw_text_with_multiple():
    c = Canvas((200, 200), font="origin_tech")
    c.draw_text("foo", 100, anchor="top-left")
    c.draw_text("bar", 100, position=(50,150))
    c.draw_text("bananarama", 200, position=(0,100))
    c.screenshot(f"{output}/canvas_draw_text_with_multiple.png")
