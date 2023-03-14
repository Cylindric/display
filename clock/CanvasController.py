import datetime
import logging
import os
from PIL import Image,ImageDraw,ImageFont

class Canvas:
    auto_flip = False

    def __init__(self, xy, font, font_size):
        logging.basicConfig(level=logging.DEBUG)
        self.fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        self.font = ImageFont.truetype(os.path.join(self.fontdir, f"{font}.ttf"), font_size)
        self.width = xy[0]
        self.height = xy[1]
        self.image = Image.new('L', xy, 255)  # 255: clear the frame
        self.canvas = ImageDraw.Draw(self.image)

    def screenshot(self, filename):
        self.image.save(filename)

    def get_image(self):
        if self.auto_flip:
            return self.image.rotate(180)
        else:
            return self.image

    def blank(self):
        self.canvas.rectangle((0, 0, self.width, self.height), fill=255) # blank

    def display_time(self, text, position, style="centre_text"):
        if style == "centre_text":
            self.draw_text_centered(text, position)

        if style == "scaled_text":
            self.draw_text_scaled_to_width(text, self.width, self.height)

    def draw_text_centered(self, text, position):
        self.canvas.text(position, text, font = self.font, fill = 0, anchor="mm")

    def draw_text_scaled_to_width(self, text, target_width, target_height):
        # Determine the size of the message in the current font
        size = self.font.getbbox(text)
        text_width = max(size)
        text_height = max(size)

        # Create a new square image the size of that message, and put the text in the middle of it
        logging.debug(f"Creating new text box {text_width}x{text_height}.")
        im = Image.new("L", (text_width, text_height), "white")
        draw = ImageDraw.Draw(im)
        draw.text((text_width//2, text_height//2), text, anchor='mm', fill="black", font=self.font)

        # Next resize that text box small enough to fit the screen
        target_size = target_width
        logging.debug(f"Resizing text box to {target_size}x{target_size}.")
        im = im.resize((target_size, target_size), resample=Image.LANCZOS)

        # Crop the new image (which will be too tall) to the screen size
        vmargin = (target_size - target_height)//2
        logging.debug(f"Screen size is ({target_width}, {target_height}).")
        logging.debug(f"Cropping new text box to (0, {vmargin}, {target_width}, {target_height-vmargin}).")
        im = im.crop((0, vmargin, target_width, target_size-vmargin))

        self.image.paste(im)


        # if style == "centre_colon":
        #     hours_text = now.strftime("%H")
        #     divider_text = ":"
        #     minutes_text = now.strftime("%M")

        #     # Because I don't want the time-colon to move around, I draw the components of the time separately
        #     # With a bit of left-align/right-align trickery, we don't really care about the size of the text
        #     divider_position = position
        #     hours_position = position + (-10, 0)
        #     minutes_position = position + (10, 0)

        #     canvas.text(hours_position, hours_text, font = font_glossy, fill = 0, anchor="rm")
        #     canvas.text(divider_position, divider_text, font = font_glossy, fill = 0, anchor="mm")
        #     canvas.text(minutes_position, minutes_text, font = font_glossy, fill = 0, anchor="lm")

