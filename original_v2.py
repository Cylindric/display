import logging
import os
import time
import sys
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5_V2

try:
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    logging.info("Full screen image...")
    Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    epd.display(epd.getbuffer(Himage))
    logging.info("READY")
    time.sleep(2)

    logging.info("Partial image...")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    Himage2.paste(bmp, (50,10))
    epd.display(epd.getbuffer(Himage2))
    logging.info("READY")
    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()
    epd.sleep()
    logging.info("Finished")

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
