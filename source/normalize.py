import sys
import os
import cv2
import numpy as np
from PIL import Image
import colorsys
import logging
import norm_composite

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

def getImg(directory,dirout=''):
    #list of images in directory
    cat1_list = os.listdir(directory)
    for f1 in cat1_list:
        full_dir1 = directory + f1
        fileout = os.path.splitext(f1)[0] + '.png'
        print ('get img file out:' + fileout)

        tmp = cv2.imread(full_dir1,cv2.IMREAD_COLOR)
        #tmp = cv2.imread("C:/Users/ashikamulagada/Documents/GitHub/SolidWasteClassification/source/trash_images/mixed/all/mixed2.JPG",cv2.IMREAD_COLOR)
        # size = tmp.size
        # print ('size: ' + size)
        try:
            size = tmp.size
            print (size)
            original = cv2.resize(tmp,(1000,1000),interpolation=cv2.INTER_CUBIC)
            normImage(original, fileout)
        except Exception as e:
            print(str(e))
            #normImage(tmp, fileout)
        #normImage(original, dirout)


def normImage(img, outdir):
#def normImage(directory,dirout=''):
    print ('Hello, world!')
    print (outdir)
    '''
    #convert to hsv
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #https://stackoverflow.com/questions/22236956/rgb-to-hsv-via-pil-and-colorsys/30346072
    #hsv = image.convert('HSV')
    #hsv = HSVColor(img)
    img2 = Image.fromarray(img.astype('uint8'), 'RGB')
    hsv = img2.convert('HSV')
    print ('Done with hsv')
    #apply clahe on V
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(cv2.UMat(hsv))
    #cv2.imwrite('clahe_2.jpg',cl1)

    print ('Done with clahe')

    #convert back to rgb space and return
    rgb = cl1.convert('RGB')

    f_out =  "1" + "_" + "normalized_bgrsegment_nobg"
    fout = os.path.join(outdir,f_out)
    cv2.imwrite(fout,rgb)

    rgb.save("normalized_img.jpg")

    return rgb
    '''
    image = np.copy(img)
    #https://stackoverflow.com/questions/25008458/how-to-apply-clahe-on-rgb-color-images
    try:
        img1 = Image.fromarray(img.astype('uint8'), 'RGB')
        image = np.copy(img1)
    except Exception as e:
        print(str(e))
    #bgr = cv2.imread(img)

    lab = cv2.cvtColor(cv2.UMat(image), cv2.COLOR_RGB2LAB)
    print ('lab')

    lab_planes = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))

    lab_planes[0] = clahe.apply(lab_planes[0])

    lab = cv2.merge(lab_planes)

    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    bgr = Image.fromarray(image.astype('uint8'), 'RGB')

    print ('normalized!')


    # bgr.save("normalized_img.jpg")

    # if imsize>1200
    #     call crop
    print('size')
    print(bgr.size)
    width, height = bgr.size
    print(width)
    if width> 1000:
        print ('calling cut')
        norm_composite.cut(outdir, bgr, 1000, 1000, 1, 1000000)
    else:
        print ('not calling cut')
        bgr.save(outdir)

        # f_out =  "1" + "_" + "normalized_images"
        # #f_out = outdir
        # fout = os.path.join(outdir,f_out)
        # cv2.imwrite(fout,bgr)


    return bgr




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


if __name__ == '__main__':
    getImg(sys.argv[2],dirout=sys.argv[3])


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
