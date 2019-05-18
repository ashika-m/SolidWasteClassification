import sys
import os
import cv2
import numpy as np
import Image, colorsys
from PIL import Image

#helper function which rotates an image
'''
input:
    1. cv image
output:
    1. image rotated 90 degrees
    2. image rotated 180 degrees
    3. image rotated 270 degrees
'''


'''
def hue_change(img, intensity, value):
    """
    Change to purple/green hue
    :param img: PIL image object
    :param intensity: float > 0.1, larger the value, the less intense and more washout
    :param value: float, the colour to hue change too on a scale from -360 to 0
    :return: PIL image object
    """
    original_width, original_height = img.size

    # Don't apply hue change if already grayscaled.
    if img.mode == 'L':
        return img

    else:
        ld = img.load()
        for y in range(original_height):
            for x in range(original_width):
                r, g, b = ld[x, y]
                h, s, v = rgb_to_hsv(r/255, g/255, b/255)
                h = (h + value/360.0) % 1.0
                s = s**intensity
                r, g, b = hsv_to_rgb(h, s, v)
                ld[x, y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999))
    return img
'''

def normImage(img):
    #convert to hsv
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #https://stackoverflow.com/questions/22236956/rgb-to-hsv-via-pil-and-colorsys/30346072
    #hsv = image.convert('HSV')
    #hsv = HSVColor(img)
    hsv = img.convert('HSV')

    #apply clahe on V
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(hsv)
    #cv2.imwrite('clahe_2.jpg',cl1)

    #convert back to rgb space and return
    rgb = cl1.convert('RGB')

    return rgb



#https://stackoverflow.com/questions/22236956/rgb-to-hsv-via-pil-and-colorsys/30346072
def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = []
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None


'''
https://stackoverflow.com/questions/50622180/does-pil-image-convertrgb-converts-images-to-srgb-or-adobergb/50623824

import io
from PIL import Image
from PIL import ImageCms

def convert_to_srgb(img):
    #Convert PIL image to sRGB color space (if possible)
    icc = img.info.get('icc_profile', '')
    if icc:
        io_handle = io.BytesIO(icc)     # virtual file
        src_profile = ImageCms.ImageCmsProfile(io_handle)
        dst_profile = ImageCms.createProfile('sRGB')
        img = ImageCms.profileToProfile(img, src_profile, dst_profile)
    return img
'''
