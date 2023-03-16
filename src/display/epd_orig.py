# *****************************************************************************
# * | File        :	  epd7in5.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0
# * | Date        :   2019-06-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import logging
from . import epdconfig

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

logger = logging.getLogger(__name__)

# COMMANDS
CMD_PANEL_SETTINGS = 0x00           # PSR   ( 1) +1byte
CMD_POWER_SETTINGS = 0x01           # PWR   ( 2) +5byte
CMD_POWER_OFF = 0x02                # POF   ( 3) no data
CMD_POWET_OFF_SEQUENCE = 0x03       # PFS   ( 4) +1byte
CMD_POWER_ON = 0x04                 # PON   ( 5) no data
CMD_POWER_ON_MEASURE = 0x05         # PMES  ( 6) no data
CMD_BOOSTER_SOFT_START = 0x06       # BTST  ( 7) +4byte
CMD_DEEP_SLEEP = 0x07               # DSLP  ( 8) +1byte
CMD_DISPLAY_START_TRANSMIT_1 = 0x10 # DTM1  ( 9) +3byte
CMD_DATA_STOP = 0x11                # DSP   (10) +1byte
CMD_DISPLAY_REFRESH = 0x12          # DRF   (11) no data
CMD_DISPLAY_START_TRANSMIT_2 = 0x13 # DTM2  (12) +3byte
CMD_DUAL_SPI = 0x15                 # 2SPI  (13) +1byte
CMD_AUTO_SEQUENCE = 0x17            # AUTO  (14) +1byte
CMD_KW_LUT  = 0x2B                  # KWOPT (15) +3byte
CMD_OSC_SETTINGS = 0x30             # PLL   (16) +1byte
CMD_VCOM = 0x50                     # CDI   (22) +2byte
CMD_TCON = 0x60                     # TCON  (25) +1byte
CMD_RESOLUTION = 0x61               # TRES  (26) +4byte
CMD_GATE_SOURCE_SETTINGS = 0x65     # GSST  (27) +4byte
CMD_GET_STATUS = 0x71               # FLG   (29) +1byte
CMD_PARTIAL_WINDOW = 0x90           # PTL   (33) +9bytes
CMD_PARTIAL_IN = 0x91               # PTIN  (34) no data
CMD_PARTIAL_OUT = 0x92              # PTOUT (35) no data

# Values to follow a CMD_PANEL_SETTINGS
PANEL_SETTINGS = 0x3F # LUT=REG, KW, UD=UP, SRC:RIGHT, BOOST:ON, RESET:NO

# Values to follow a CMD_POWER_SETTINGS
POWER_SETTING_BDEN_VSREN_VSEN_VGEN = 0x17 # BD_EN=1, VSR_EN=1, VS_EN=1, VG_EN=1
POWER_SETTING_SLEW_VGH20_VGL20 = 0x17     # VPP_EN=0, SLEW=1, VGH=20V, VGL=-20V
POWER_SETTING_VDH15 = 0x3F                # VDH=15V
POWER_SETTING_VDL15 = 0x3F                # VDL=-15V
POWER_SETTING_VDHR = 0x11                 # VDHR=5.8V

# Values to follow a CMD_OSC_SETTINGS
OSC_PLL = 0x6 # 3C=50Hz, 3A=100HZ

# Values to follow a CMD_DEEP_SLEEP
DEEP_SLEEP_CHECK_CODE = 0xA5

class EPD:
    Voltage_Frame_7IN5_V2 = [
      # OSC   VSH   VSL   VSHR  VCOM        VGH&VGL
	    0x06, 0x3F, 0x3F, 0x11, 0x24, 0x07, 0x17,
    ]

    LUT_VCOM_7IN5_V2 = [
        0x00, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x0F, 0x01, 0x0F, 0x01, 0x02,
        0x00, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ] 

    LUT_WW_7IN5_V2 = [
        0x10, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x84, 0x0F, 0x01, 0x0F, 0x01, 0x02,
        0x20, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_BW_7IN5_V2 = [
        0x10, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x84, 0x0F, 0x01, 0x0F, 0x01, 0x02,
        0x20, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_WB_7IN5_V2 = [
        0x80, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x84, 0x0F, 0x01, 0x0F, 0x01, 0x02,
        0x40, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    LUT_BB_7IN5_V2 = [
        0x80, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x84, 0x0F, 0x01, 0x0F, 0x01, 0x02,
        0x40, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    #--------------------------------------------------------------------------------------------

    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data2(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        logger.debug("e-Paper busy")
        self.send_command(CMD_GET_STATUS)
        busy = epdconfig.digital_read(self.busy_pin)
        while(busy == 0):
            self.send_command(CMD_GET_STATUS)
            busy = epdconfig.digital_read(self.busy_pin)
        epdconfig.delay_ms(20)
        logger.debug("done.")

    def SetLut(self, lut_vcom, lut_ww, lut_bw, lut_wb, lut_bb):
        self.send_command(0x20)
        for count in range(0, 42):
            self.send_data(lut_vcom[count])

        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(lut_ww[count])

        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(lut_bw[count])

        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(lut_wb[count])

        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(lut_bb[count])

    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()

        self.send_command(CMD_POWER_SETTINGS)
        self.send_data(0x17)        # 1-0=11: internal power
        self.send_data(self.Voltage_Frame_7IN5_V2[6])   # VGH&VGL
        self.send_data(self.Voltage_Frame_7IN5_V2[1])   # VSH
        self.send_data(self.Voltage_Frame_7IN5_V2[2])   # VSL
        self.send_data(self.Voltage_Frame_7IN5_V2[3])   # VSHR

        self.send_command(0x82)     # VCOM DC Setting
        self.send_data(self.Voltage_Frame_7IN5_V2[4])   # VCOM

        self.send_command(CMD_BOOSTER_SOFT_START)
        self.send_data(0x27)
        self.send_data(0x27)
        self.send_data(0x2F)
        self.send_data(0x17)

        self.send_command(CMD_OSC_SETTINGS)
        self.send_data(OSC_PLL)

        self.send_command(CMD_POWER_ON)
        epdconfig.delay_ms(100)
        self.ReadBusy()

        self.send_command(CMD_PANEL_SETTINGS)
        self.send_data(PANEL_SETTINGS)

        self.send_command(CMD_RESOLUTION)
        self.send_data(0x03)        # source 800
        self.send_data(0x20)
        self.send_data(0x01)        # gate 480
        self.send_data(0xE0)

        self.send_command(CMD_DUAL_SPI)
        self.send_data(0x00)        # MM_EN, DUSPI_EN disabled

        self.send_command(CMD_VCOM)
        self.send_data(0x10)
        self.send_data(0x07)

        self.send_command(CMD_TCON)
        self.send_data(0x22)

        self.send_command(CMD_GATE_SOURCE_SETTINGS)
        self.send_data(0x00)
        self.send_data(0x00)        # 800*480
        self.send_data(0x00)
        self.send_data(0x00)

        self.SetLut(self.LUT_VCOM_7IN5_V2, self.LUT_WW_7IN5_V2, self.LUT_BW_7IN5_V2, self.LUT_WB_7IN5_V2, self.LUT_BB_7IN5_V2)
        # EPD hardware init end
        return 0

    def getbuffer(self, image):
        img = image
        imwidth, imheight = img.size
        if(imwidth == self.width and imheight == self.height):
            img = img.convert('1')
        elif(imwidth == self.height and imheight == self.width):
            # image has correct dimensions, but needs to be rotated
            img = img.rotate(90, expand=True).convert('1')
        else:
            logger.warning("Wrong image dimensions: must be " + str(self.width) + "x" + str(self.height))
            # return a blank buffer
            return [0x00] * (int(self.width/8) * self.height)

        buf = bytearray(img.tobytes('raw'))
        # The bytes need to be inverted, because in the PIL world 0=black and 1=white, but
        # in the e-paper world 0=white and 1=black.
        for i in range(len(buf)):
            buf[i] ^= 0xFF
        return buf

    def display(self, image):
        self.send_command(CMD_DISPLAY_START_TRANSMIT_2)
        self.send_data2(image)
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()

    def clear(self):
        buf = [0x00] * (int(self.width/8) * self.height)
        self.send_command(CMD_DISPLAY_START_TRANSMIT_1)
        self.send_data2(buf)
        self.send_command(CMD_DISPLAY_START_TRANSMIT_2)
        self.send_data2(buf)
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()

    def sleep(self):
        self.send_command(CMD_POWER_OFF)
        self.ReadBusy()
        self.send_command(CMD_DEEP_SLEEP)
        self.send_data(DEEP_SLEEP_CHECK_CODE)
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()

    def test_partial(self, image, position, size):
        self.send_command(CMD_PARTIAL_WINDOW)
        self.send_data(0x00) # HRST
        self.send_data(0x00) # HRST
        self.send_data(0x03) # HRED
        self.send_data(0x1F) # HRED
        self.send_data(0x00) # VRST
        self.send_data(0x00) # VRST
        self.send_data(0x00) # VRED
        self.send_data(0x57) # VRED
        self.send_data(0x01) # PT_SCAN=BOTH
        self.send_command(CMD_PARTIAL_IN)
        self.send_data2(image)
        self.send_command(CMD_PARTIAL_OUT)
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()
