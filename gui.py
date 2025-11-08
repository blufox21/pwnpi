import numpy as np
from PIL import Image, ImageDraw, ImageFont

class Gui:
    def __init__(self, disp):
        self.display = disp 
        self.main_menu = []

        self.BG_COLOR = (20,10,10)

        self.HEAD_COLOR = (25, 15, 15)
        self.OUTLINE = (200, 200, 200)
        self.HEAD_HEIGHT = 32

        self.img = Image.new("RGB", (self.display.WIDTH, self.display.HEIGHT), self.BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)

        self.draw.rectangle([0,0, self.display.WIDTH-1, self.display.HEIGHT-1], fill=self.BG_COLOR, outline=self.OUTLINE)
        # header bg
        self.draw.rectangle([0, 0, self.display.WIDTH-1, self.HEAD_HEIGHT], fill=self.HEAD_COLOR, outline=self.OUTLINE)

    def get(self):
        img = np.array(self.img.convert('RGB'))
        pb = np.rot90(img, self.display.ROTATION // 90).astype("uint16")

        x1 = ((pb[..., [0]] & 0xF8) | (pb[..., [1]] >> 5)).flatten()
        x2 = (((pb[..., [1]] & 0x1C) << 3) | (pb[..., [2]] >> 3)).flatten()

        res1 = []

        for i in range(len(x1)):
            res1.append(int(x1[i]))
            res1.append(int(x2[i]))

        return res1

