"""This module provides for managing a grapgical Canvas"""
import logging
import os
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class Canvas:
    """
    This class provides an interface to the the drawing tools needed for the display.
    """

    def __init__(self, screen_size, font=None, font_size=300):
        logging.basicConfig(level=logging.DEBUG)
        self.auto_flip = False
        self._fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        self._font = None
        if font:
            self._font = ImageFont.truetype(os.path.join(self._fontdir, f"{font}.ttf"), font_size)
        self._full_size = screen_size
        self._margin_left = 0
        self._margin_right = 0
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
        elif filename.endswith(".jpg"):
            self._image.save(filename)
        else:
            raise RuntimeError("Invalid filename, must be either *.png or *.jpg")

    def get_image(self):
        """Returns the current Image"""

        if self.auto_flip:
            return self._image.rotate(180)
        else:
            return self._image

    def blank(self):
        """Blanks the whole current canvas, ignoring any margins set."""

        self._canvas.rectangle((0, 0, self._full_size[0], self._full_size[1]), fill=255) # blank

    def create_text_object(self, text, width=0, height=0) -> Image:
        """Creates a new Image object with the specified text, scaled
        to either the width or the height given.
        Either width or height must be specified.

        Args:
            text (str): The text to draw
            width (int, optional): The target width. Defaults to 0.
            height (int, optional): The target height. Defaults to 0.

        Returns:
            Image: image with the scaled text
        """
        if width <= 0 and height <= 0:
            raise ValueError("Invalid scale, one of width or height must be >0")
        if width > 0 and height > 0:
            raise ValueError("Invalid scale, only one width or height must be specified")

        # Determine the size of the message in the current font
        size = self._font.getbbox(text)
        text_width = size[2]
        text_height = size[3]

        # Determine the ratio to scale the text by to get to the desired width
        if width > 0:
            scale = width / text_width
        else:
            scale = height / text_height
        new_width = int(text_width * scale)
        new_height = int(text_height * scale)

        # Create a new image the size of the text, and put the text in the middle of it
        logging.debug("Creating new text box %sx%s.", text_width, text_height)
        img = Image.new("L", (text_width, text_height), "white")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, anchor='la', fill="black", font=self._font)

        # Next resize the text to the desired dimentions
        logging.debug("Resizing text box to %sx%s.", new_width, new_height)
        img = img.resize((new_width, new_height), resample=Image.LANCZOS)

        return img

    def draw_text(self, text, width, position=(0,0), anchor="baseline"):
        glyph = self.create_text_object(text, width)

        if anchor == "top-left":
            pass
        elif anchor == "baseline":
            position = (
                position[0],
                position[1] - glyph.height
            )
        elif anchor == "centre":
            position = (
                position[0] - (glyph.width//2),
                position[1] - (glyph.height//2)
            )

        # Place the text at the requested position
        self._image.paste(glyph, position)

    def paste(self, img, position=(0,0)):
        """Paste the supplied Image or Canvas into this Canvas.

        Args:
            img (Image or Canvas): the image to paste
            position (tuple, optional): The location to paste the image to.
                                        Defaults to (0,0).
        """
        if isinstance(img, Canvas):
            self._image.paste(img.get_image(), position)
        else:
            self._image.paste(img, position)
