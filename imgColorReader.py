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
        hueName = ImgColorReader.hue_to_name(hsv[0] * 360)

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
    def rgb_to_hsl(rgb):
        R = float(rgb[0])
        G = float(rgb[1])
        B = float(rgb[2])

        var_R = ( R / 255 )                     #RGB from 0 to 255
        var_G = ( G / 255 )
        var_B = ( B / 255 )
        print((var_R,var_G,var_B))

        var_Min = min( var_R, var_G, var_B )    #Min. value of RGB
        var_Max = max( var_R, var_G, var_B )    #Max. value of RGB
        del_Max = var_Max - var_Min             #Delta RGB value

        L = ( var_Max + var_Min ) / 2

        if ( del_Max == 0 ):                    #This is a gray, no chroma...

           H = 0                                #HSL results from 0 to 1
           S = 0

        else:                            #Chromatic data...
            if ( L < 0.5 ):
               S = del_Max / ( var_Max + var_Min )
            else:
               S = del_Max / ( 2 - var_Max - var_Min )

            del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
            del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
            del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max

            if ( var_R == var_Max ):
               H = del_B - del_G
            elif (var_G == var_Max):
                H = ( 1 / 3 ) + del_R - del_B
            elif ( var_B == var_Max ):
                H = ( 2 / 3 ) + del_G - del_R

            if ( H < 0 ):
                H = H+ 1
            if ( H > 1 ):
                H =H- 1

        H = int(H*360)
        S = int(S*360)
        L = int(L*360)
        return (H,S,L)

    @staticmethod
    def hue_to_name(hue):
        if (hue<20 or hue>330):
            return "red"
        elif (hue<50):
            return "orange"
        elif (hue<70):
            return "yellow"
        elif (hue<150):
            return "green"
        elif (hue<280):
            return "blue"
        elif (hue<320):
            return "pink"
