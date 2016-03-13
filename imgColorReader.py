from PIL import Image
from PIL import ImageDraw
from colorthief import ColorThief
import cv2

import time
import colorsys

class ImgColorReader(object):

    @staticmethod
    def readMainColorOfPicture(frame):
        frame = cv2.flip(frame,1)
        height, width, channels = frame.shape

        frame = frame[height/3:height*2/3,width/3:width*2/3]
        pil_im = Image.fromarray(frame)
        color_thief = ColorThief(pil_im)
        rgb=color_thief.get_color(quality=1)
        # print(rgb)
        # print(ColorReader.rgb_to_hsl(rgb))
        # print(color_thief.get_palette(quality=1))
        hsv = ImgColorReader.rgb_to_hue(rgb)
        # print(hsv[0]*360)
        hue = hsv[0] * 360
        print(hue)
        hueName = ImgColorReader.hue_to_name(hue)

        draw = ImageDraw.Draw(pil_im)
        box = (0,0,40,40)
        draw.rectangle(box,rgb)
        del draw
        # pil_im.show()
        return hueName

    @staticmethod
    def rgb_to_hue(rgb):
        R = float(rgb[0])
        G = float(rgb[1])
        B = float(rgb[2])
        return colorsys.rgb_to_hsv(R, G, B)


    @staticmethod
    def hue_to_name(hue):
        if (hue<10 or hue>330):
            return "red"
        elif (hue<40):
            return "orange"
        elif (hue<70):
            return "yellow"
        elif (hue<150):
            return "green"
        elif (hue<280):
            return "blue"
        else:
            return "pink"

