import spidev
import time
import RPi.GPIO as GPIO

RES_PIN = 25
DC_PIN = 24
BLK_PIN = 27

class ST7789:
    def __init__(self, w=240, h=240, res=25, dc=24, blk=27, x_off=0, y_off=0, rot=0):
        self.WIDTH = w
        self.HEIGHT = h
        
        self.RES_PIN = res
        self.DC_PIN = dc
        self.BLK_PIN = blk
        
        self.ROTATION = rot

        self.x_off = x_off
        self.y_off = y_off

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RES_PIN, GPIO.OUT)
        GPIO.setup(self.DC_PIN, GPIO.OUT)
        GPIO.setup(self.BLK_PIN, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 50000000
        self.spi.mode = 0b11
        self.init_display()

    def write_command(self, cmd):
        GPIO.output(self.DC_PIN, GPIO.LOW)
        self.spi.writebytes([cmd])

    def write_data(self, data):
        GPIO.output(self.DC_PIN, GPIO.HIGH)
        if isinstance(data,list):
            self.spi.writebytes(bytearray(data))
        else:
            self.spi.writebytes(bytearray([data]))

    def hard_reset(self):
        GPIO.output(self.RES_PIN, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.RES_PIN, GPIO.HIGH)
        time.sleep(0.1)

    def init_display(self):
        self.hard_reset()

        self.write_command(0x11)
        time.sleep(0.12)
        
        # memory data access control
        self.write_command(0x36)
        self.write_data(0x00)
        
        # interface pixel format
        self.write_command(0x3A)
        self.write_data(0x55)

        # Display inversion on
        self.write_command(0x21)

        # cloumn address set
        self.write_command(0x2A)
        self.write_data([0x00, 0x00, 0x00, 0xEF])

        # row address set
        self.write_command(0x2B)
        self.write_data([0x00, 0x00, 0x00, 0xEF])

        # turn on
        self.write_command(0x29)

        # backlight
        GPIO.output(self.BLK_PIN, GPIO.HIGH)

        time.sleep(0.1)

    def set_window(self, x0, y0, x1, y1):
        self.write_command(0x2A)

        x0 += self.x_off
        x1 += self.x_off
        y0 += self.y_off
        y1 += self.y_off

        self.write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])

        self.write_command(0x2B)
        self.write_data([y0 >>8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])

        # write memory
        self.write_command(0x2C)
    
    def display(self, pixel_data, chunk_size=4096):
        self.set_window(0,0, self.WIDTH-1, self.HEIGHT-1)       
        GPIO.output(self.DC_PIN, GPIO.HIGH)
        for i in range(0, len(pixel_data), chunk_size):
            chunk = pixel_data[i:i + chunk_size]
            self.spi.writebytes(chunk)


    def fill(self, color):
        color_high = (color >> 8) & 0xFF
        color_low = color & 0xFF
        
        pixel_data = [color_high, color_low] * (self.WIDTH * self.HEIGHT)
        
        self.display(pixel_data)

    def cleanup(self):
        GPIO.output(self.BLK_PIN, GPIO.LOW)

        self.spi.close()

        GPIO.cleanup()
