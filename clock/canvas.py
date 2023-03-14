import logging
import os
from PIL import Image, ImageDraw, ImageFont

class Canvas:
    """
    This class provides an interface to the the drawing tools needed for the display.
    """

    def __init__(self, screen_size, font, font_size):
        logging.basicConfig(level=logging.DEBUG)
        self._auto_flip = True
        self._fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        self._font = ImageFont.truetype(os.path.join(self._fontdir, f"{font}.ttf"), font_size)
        self._full_size = screen_size
        self._margin_left = 50
        self._margin_right = 50
        self._width = screen_size[0] - self._margin_left - self._margin_right
        self._height = screen_size[1]
        self._image = Image.new('L', screen_size, 255)  # 255: clear the frame
        self._canvas = ImageDraw.Draw(self._image)

    def screenshot(self, filename):
        """
        Saves a screen-shot of the current Image to the specified filename.
        If the filename looks like a PNG, it will replace white pixels with 
        transparent ones.
        """
        if filename.endswith(".png"):
            img = self._image.convert('RGBA')
            datas = img.getdata()
            new_data = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            img.save(filename)
        else:
            self._image.save(filename)

    def get_image(self):
        """Returns the current Image"""

        if self._auto_flip:
            return self._image.rotate(180)
        else:
            return self._image

    def blank(self):
        """Blanks the whole current canvas, ignoring any margins set."""

        self._canvas.rectangle((0, 0, self._full_size[0], self._full_size[1]), fill=255) # blank

    def display_time(self, text, position, style="centre_text"):
        if style == "centre_text":
            self.draw_text_centered(text, position)

        if style == "scaled_text":
            self.draw_text_scaled_to_width(text, self._width, self._height)

    def draw_text_centered(self, text, position):
        self._canvas.text(position, text, font = self._font, fill = 0, anchor="mm")

    def draw_text_scaled_to_width(self, text, target_width, target_height):
        # Determine the size of the message in the current font
        size = self._font.getbbox(text)
        text_width = max(size)
        text_height = max(size)

        # Create a new square image the size of that message, and put the text in the middle of it
        logging.debug("Creating new text box %sx%s.", text_width, text_height)
        img = Image.new("L", (text_width, text_height), "white")
        draw = ImageDraw.Draw(img)
        draw.text((text_width//2, text_height//2), text, anchor='mm', fill="black", font=self._font)

        # Next resize that text box small enough to fit the screen
        target_size = target_width
        logging.debug("Resizing text box to %sx%s.", target_size, target_size)
        img = img.resize((target_size, target_size), resample=Image.LANCZOS)

        # Crop the new image (which will be too tall) to the screen size
        vmargin = (target_size - target_height)//2
        logging.debug("Screen size is (%sx%s).", target_width, target_height)
        logging.debug(
            "Cropping new text box to (0, %s, %s, %s).",
            vmargin,
            target_width,
            target_height-vmargin)

        img = img.crop((0, vmargin, target_width, target_size-vmargin))

        self._image.paste(img, (self._margin_left, 0))
