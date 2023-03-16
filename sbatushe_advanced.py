import logging
import os
import time
import sys
from PIL import Image

logging.basicConfig(level=logging.INFO)

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5_V2_Sbatushe

try:
    base_image = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    base_image.save("test01-base.png")

    sprite_image = Image.open(os.path.join(picdir, '100x100.bmp'))
    sprite_image.save("test01-sprite.png")

    output_image = base_image.copy()
    output_image.paste(sprite_image, (375,215))
    output_image.save("test01-output1.png")

    for y in range(output_image.size[1]):
        for x in range(output_image.size[0]):
            p = output_image.getpixel((x,y))
            if p >= 127:
                output_image.putpixel((x,y), 1)
    output_image.save("test01-output2.png")

    print("Starting screen...")
    epd = epd7in5_V2_Sbatushe.EPD()
    epd.init()
    epd.Clear()
    print("READY")

    print("Showing first image...")
    epd.display(epd.getbuffer(base_image))
    print("READY")
    time.sleep(2)

    print("Showing second merged image...")
    epd.display(epd.getbuffer(output_image))
    print("READY")
    time.sleep(2)

    print("Showing flipping images...")
    epd.display(epd.getbuffer(output_image))
    print("next")
    epd.display(epd.getbuffer(base_image))
    print("next")
    epd.display(epd.getbuffer(output_image))
    print("next")
    epd.display(epd.getbuffer(base_image))
    print("next")
    epd.display(epd.getbuffer(output_image))
    print("next")
    epd.display(epd.getbuffer(base_image))
    print("READY")
    time.sleep(2)

    print("Clearing...")
    epd.init()
    epd.Clear()
    epd.sleep()
    print("Finished")

except IOError as e:
    print(e)

except KeyboardInterrupt:    
    print("ctrl + c:")
    epd7in5_V2_Sbatushe.epdconfig.module_exit()
    exit()
