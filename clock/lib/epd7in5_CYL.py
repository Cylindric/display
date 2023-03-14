# *****************************************************************************
# * | File        :	  epd7in5_CYL.py
# * | Author      :   Waveshare team, Emanuele Sabato, Mark Hanford
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.0-CYL
# * | Date        :   2023-03-13
# # | Info        :   Modified from python demo for partial-refresh
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

# COMMANDS
CMD_PANEL_SETTINGS = 0x00
CMD_POWER_SETTINGS = 0x01
CMD_POWER_OFF = 0x02
CMD_POWER_ON = 0x04
CMD_DEEP_SLEEP = 0x07
CMD_DISPLAY_START_TRANSMIT_1 = 0x10
CMD_DISPLAY_REFRESH = 0x12
CMD_DISPLAY_START_TRANSMIT_2 = 0x13

# Values to follow a CMD_PANEL_SETTINGS
PANEL_SETTING_ = 0xBF # KW-3f KWR-2F BWROTP 0f, BWOTP 1f

# Values to follow a CMD_POWER_SETTINGS
POWER_SETTING_VSREN_VSEN_VGEN = 0x07 # VSR_EN=1, VS_EN=1, VG_EN=1
POWER_SETTING_VGH20_VGL20 = 0x07     # VGH=20V, VGL=-20V
POWER_SETTING_VDH15 = 0x3f           # VDH=15V
POWER_SETTING_VDL15 = 0x3f           # VDL=-15V

# Values to follow a CMD_DEEP_SLEEP
DEEP_SLEEP_CHECK_CODE = 0xA5


class EPD:
    lut_vcom0 = [ 
    0x00, 0x17, 0x00, 0x00, 0x00, 0x02,        
    0x00, 0x17, 0x17, 0x00, 0x00, 0x02,        
    0x00, 0x0A, 0x01, 0x00, 0x00, 0x01,        
    0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_ww = [
    0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bw = [
    0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_wb = [
    0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bb = [
    0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
    0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #-----------PARTIAL REFRESH HOMEMADE -----------------------------------------------------
    EPD_4IN2_Partial_lut_vcom1 =[
    0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]

    EPD_4IN2_Partial_lut_ww1 =[
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_bw1 =[
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_wb1 =[
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,    
    ]    

    EPD_4IN2_Partial_lut_bb1 =[
    0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
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
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)   

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
        logging.debug("e-Paper busy...")
        self.send_command(0x71)
        busy = epdconfig.digital_read(self.busy_pin)
        while(busy == 0):
            self.send_command(0x71)
            busy = epdconfig.digital_read(self.busy_pin)
        epdconfig.delay_ms(200)
        logging.debug("done.")

    def set_lut(self):
        self.send_command(0x20)               # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom0[count])
            
        self.send_command(0x21)         # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
            
        self.send_command(0x22)         # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
            
        self.send_command(0x23)         # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
            
        self.send_command(0x24)         # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
        
    def Partial_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):	     
            self.send_data(self.EPD_4IN2_Partial_lut_vcom1[count])

        self.send_command(0x21)
        for count in range(0, 42):	     
            self.send_data(self.EPD_4IN2_Partial_lut_ww1[count])
        
        self.send_command(0x22)
        for count in range(0, 42):     
            self.send_data(self.EPD_4IN2_Partial_lut_bw1[count])

        self.send_command(0x23)
        for count in range(0, 42):	     
            self.send_data(self.EPD_4IN2_Partial_lut_wb1[count])

        self.send_command(0x24)
        for count in range(0, 42):	     
            self.send_data(self.EPD_4IN2_Partial_lut_bb1[count])        
        
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        
        self.send_command(CMD_POWER_SETTINGS)         # POWER SETTING
        self.send_data(POWER_SETTING_VSREN_VSEN_VGEN) # VSR_EN=1, VS_EN=1, VG_EN=1
        self.send_data(POWER_SETTING_VGH20_VGL20)     # VGH=20V,VGL=-20V
        self.send_data(POWER_SETTING_VDH15)		      # VDH=15V
        self.send_data(POWER_SETTING_VDL15)		      # VDL=-15V

        self.send_command(CMD_POWER_ON)     # POWER ON
        epdconfig.delay_ms(100)
        self.ReadBusy()

        self.send_command(CMD_PANEL_SETTINGS)     # PANNEL SETTING
        self.send_data(0xBF)        # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x30)     # PLL setting
        self.send_data(0x3c)        # 3A 100HZ   29 150Hz 39 200HZ  31 171HZ

        self.send_command(0x61)     # tres
        self.send_data(0x03)		# source 800
        self.send_data(0x20)
        self.send_data(0x01)		# gate 480
        self.send_data(0xE0)

        self.send_command(0X15)     # DUAL SPI
        self.send_data(0x00)        # MM_EN, DUSPI_EN disabled

        self.send_command(0X50)     # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x10)
        self.send_data(0x07)

        self.send_command(0X60)     # TCON SETTING
        self.send_data(0x22)
        
        #self.set_lut()
        self.Partial_SetLut()
        # EPD hardware init end
        return 0

    def getbuffer(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if(imwidth == self.width and imheight == self.height):
            # logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            # logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf
        
    def display(self, image):
        self.Partial_SetLut()
        self.send_command(CMD_DISPLAY_START_TRANSMIT_2)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(~image[i])
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()
        
    def display_window(self, image, height):
        self.send_command(CMD_DISPLAY_START_TRANSMIT_2)
        for i in range(0, int(self.width * height / 8)):
            self.send_data(~image[i]);
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()
        
    def Clear(self):
        self.send_command(CMD_DISPLAY_START_TRANSMIT_1)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0x00)
            
        self.send_command(CMD_DISPLAY_START_TRANSMIT_2)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0x00)
                
        self.send_command(CMD_DISPLAY_REFRESH)
        epdconfig.delay_ms(100)
        self.ReadBusy()

    def sleep(self):
        self.send_command(CMD_POWER_OFF)
        self.ReadBusy()
        self.send_command(CMD_DEEP_SLEEP)
        self.send_data(DEEP_SLEEP_CHECK_CODE)
        epdconfig.module_exit()
