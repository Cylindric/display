import logging
import os
from PIL import Image, ImageDraw, ImageFont

class Canvas:

    def __init__(self, xy, font, font_size):
        logging.basicConfig(level=logging.DEBUG)
        self._auto_flip = True
        self._fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        self._font = ImageFont.truetype(os.path.join(self._fontdir, f"{font}.ttf"), font_size)
        self._full_size = xy
        self._margin_left = 50
        self._margin_right = 50
        self._width = xy[0] - self._margin_left - self._margin_right
        self._height = xy[1]
        self._image = Image.new('L', xy, 255)  # 255: clear the frame
        self._canvas = ImageDraw.Draw(self._image)

    def screenshot(self, filename):
        if filename.endswith(".png"):
            img = self._image.convert('RGBA')
            datas = img.getdata()
            newData = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            img.save(filename)
        else:
            self._image.save(filename)

    def get_image(self):
        if self._auto_flip:
            return self._image.rotate(180)
        else:
            return self._image

    def blank(self):
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
        logging.debug(f"Creating new text box {text_width}x{text_height}.")
        im = Image.new("L", (text_width, text_height), "white")
        draw = ImageDraw.Draw(im)
        draw.text((text_width//2, text_height//2), text, anchor='mm', fill="black", font=self._font)

        # Next resize that text box small enough to fit the screen
        target_size = target_width
        logging.debug(f"Resizing text box to {target_size}x{target_size}.")
        im = im.resize((target_size, target_size), resample=Image.LANCZOS)

        # Crop the new image (which will be too tall) to the screen size
        vmargin = (target_size - target_height)//2
        logging.debug(f"Screen size is ({target_width}, {target_height}).")
        logging.debug(f"Cropping new text box to (0, {vmargin}, {target_width}, {target_height-vmargin}).")
        im = im.crop((0, vmargin, target_width, target_size-vmargin))

        self._image.paste(im, (self._margin_left, 0))
