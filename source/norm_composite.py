import sys
import os
import cv2
import numpy as np
import colorsys
from PIL import Image
import normalize


def getImages(directory1,directory2,directory3,dirout=''):
    #list of images in directory
    cat2_list = os.listdir(directory2)
    for f2 in cat2_list:
        full_dir2 = directory2 + f2
        fileout = os.path.splitext(f2)[0] + '.png'
        print ('get img file out:' + fileout)

        tmp2 = cv2.imread(full_dir2,cv2.IMREAD_COLOR)

    cat3_list = os.listdir(directory3)
    for f3 in cat3_list:
        full_dir3 = directory3 + f3
        fileout = os.path.splitext(f3)[0] + '.png'
        print ('get img file out:' + fileout)

        tmp3 = cv2.imread(full_dir3,cv2.IMREAD_COLOR)

    # cat2_list = os.listdir(directory2)[0]
    # print ('cat2_list')
    # print (cat2_list)
    # full_dir2 = directory2 + cat2_list
    # fileout = os.path.splitext(cat2_list)[0] + '.png'
    # print ('get img file out:' + fileout)
    # tmp2 = cv2.imread(full_dir2,cv2.IMREAD_COLOR)
    #
    # cat3_list = os.listdir(directory3)[0]
    # full_dir3 = directory3 + cat3_list
    # print ('full_dir3')
    # print (full_dir3)
    # fileout = os.path.splitext(cat3_list)[0] + '.png'
    # print ('get img file out:' + fileout)
    # tmp3 = cv2.imread(full_dir3,cv2.IMREAD_COLOR)


    cat1_list = os.listdir(directory1)
    for f1 in cat1_list:
        full_dir1 = directory1 + f1
        fileout = os.path.splitext(f1)[0] + '.png'
        print ('get img file out:' + fileout)
        tmp1 = cv2.imread(full_dir1,cv2.IMREAD_COLOR)
        try:
            print ('resizing cardboard')
            original1 = cv2.resize(tmp1,(1000,1000),interpolation=cv2.INTER_CUBIC)
            print ('resizing treematter')
            original2 = cv2.resize(tmp2,(1000,1000),interpolation=cv2.INTER_CUBIC)
            print ('resizing plywood')
            original3 = cv2.resize(tmp3,(1000,1000),interpolation=cv2.INTER_CUBIC)
            stitch(original1, original2, original3, fileout)
        except Exception as e:
            print(str(e))
        #normImage(original, dirout)


#https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
def stitch(img1, img2, img3, fileout):
    print ('Stitching')
    #images = map(Image.open, ['Test1.jpg', 'Test2.jpg', 'Test3.jpg'])
    image1 = Image.fromarray(img1.astype('uint8'), 'RGB')
    image2 = Image.fromarray(img2.astype('uint8'), 'RGB')
    image3 = Image.fromarray(img3.astype('uint8'), 'RGB')

    image1.save('image1_test.jpg')

    images = [image1, image2, image3]

    print ('map')
    print (images)
    '''
    widths, heights = zip((i.size for i in images))
    print ('zip')

    total_width = sum(widths)
    max_height = max(heights)
    '''

    print ('New im')
    new_im = Image.new('RGB', (3000, 1000))

    x_offset = 0
    print ('for')
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    new_im.save('test.jpg')
    print ('saved')

    normalize.normImage(new_im, fileout)

    return new_im




#https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python
def cut(path, image, height, width, k, area):
    print ('cutting')
    # im = Image.open(image)
    # print ('opened')
    image.save(str(k)+path)
    imgwidth, imgheight = image.size
    #for i in range(0,imgheight,height):
    for j in range(0,imgwidth,width):
        print ('in loop')
        box = (j, 0, j+width, height)
        a = image.crop(box)
        print ('croped box')
        try:
            o = a.crop(area)
            print ('croped area')
            o.save('k' + path)
            print ('saved')
            #o.save(os.path.join(path,"PNG","IMG-%s.png" % k))
        # except:
        #     pass
        except Exception as e:
            print('e: ' + str(e))
            #a.save(str(k) + path)
            print('saved')
        k +=1



if __name__ == '__main__':
    getImages(sys.argv[2],sys.argv[3],sys.argv[4],dirout=sys.argv[5])
