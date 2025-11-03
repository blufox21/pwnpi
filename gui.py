from PIL import Image, ImageDraw, ImageFont

class Gui:
    def __init__(self, disp):
        self.display = disp 
        self.main_menu = []

        self.BG_COLOR = (255,249,238)

        self.HEAD_COLOR = (250, 255, 254)
        self.HEAD_OUTLINE = (32, 32, 32)
        self.HEAD_HEIGHT = 32

        self.img = Image.new("RGB", (self.display.WIDTH, self.display.HEIGHT), self.BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)

        # header bg
        self.draw.rectangle([0, 0, self.display.WIDTH, self.HEAD_HEIGHT], fill=self.HEAD_COLOR, outline=HEAD_OUTLINE)
        self.img.show()
