import cv2
import numpy as np
import random
import os
import re
import math
import constants
import scipy.misc
from segmentModule import *
from matplotlib import pyplot as plt

#reads in training image for cnn using pixel data as the training set
#28 x 28 surrounding area of each pixel used for training
#3x3 conv, 7x7 conv
#all training images must be passed when calling nn.py

def cnn_readOneImg2(image_dir):
    inputs = []
    img = cv2.imread(image_dir,cv2.IMREAD_COLOR)
    original,markers = getSegments(img,False)
    uniqueMarkers = np.unique(markers)
    canvas = original.copy()
    for uq_mark in uniqueMarkers:
        #make a canvas and paint each unique segment
        b = random.randint(0,255)
        g = random.randint(0,255)
        r = random.randint(0,255)
        canvas[markers == uq_mark] = [b,g,r]

    return(canvas,markers)

#gets n patches from an image with its respective label
def getTestingBatch(n,catname='mixed'):
    cats = ['treematter','plywood','cardboard','bottles','trashbag','blackbag']
    random.seed(None)
    inputs = []
    labels = []

    #initialize variables
    tmp = cv2.imread(constants.MIXEDFILE,cv2.IMREAD_COLOR)
    print ("img size")
    print (tmp.size)
    img = cv2.resize(tmp,(constants.FULL_IMGSIZE,constants.FULL_IMGSIZE),interpolation=cv2.INTER_CUBIC)
    tmp = cv2.imread(constants.GROUND_TRUTH,cv2.IMREAD_COLOR)
    gt = cv2.resize(tmp,(constants.FULL_IMGSIZE,constants.FULL_IMGSIZE),interpolation=cv2.INTER_NEAREST)

    #preprocess label image to be of 2^3 color scheme
    gt[gt <= 128] = 0
    gt[gt > 128] = 255

    #get pixel batch
    w, h, d = img.shape
    for j in range(n):
        low = int(constants.IMG_SIZE / 2)
        high = int(w - (constants.IMG_SIZE / 2) - 1)
        a = random.randint(low,high)
        b = random.randint(low,high)
        box_low1 = int(a - (constants.IMG_SIZE / 2))
        box_low2 = int(b - (constants.IMG_SIZE / 2))
        box_high1 = int(a + (constants.IMG_SIZE / 2))
        box_high2 = int(b + (constants.IMG_SIZE / 2))

        #get the box
        box = img[box_low1:box_high1,box_low2:box_high2,:]
        inputs.append(box)

        #get label
        if np.all(gt[a,b] == [0,0,255]):
            labels.append(constants.CAT1_ONEHOT)
        elif np.all(gt[a,b] == [0,255,0]):
            labels.append(constants.CAT2_ONEHOT)
        elif np.all(gt[a,b] == [255,0,0]):
            labels.append(constants.CAT3_ONEHOT)
        elif np.all(gt[a,b] == [0,255,255]):
            labels.append(constants.CAT4_ONEHOT)
        elif np.all(gt[a,b] == [255,0,255]):
            labels.append(constants.CAT5_ONEHOT)
        elif np.all(gt[a,b] == [255,255,0]):
            labels.append(constants.CAT6_ONEHOT)
        else:
            print(gt[a,b])
            print('error with label image')

    #shuffle the input and labels in parralel
    c = list(zip(inputs,labels))
    random.shuffle(c)
    inputs,labels = zip(*c)
    inputs = np.array(inputs)[:n,:,:,:]
    labels = np.array(labels)[:n]
    cat1label = np.zeros(len(labels))
    cat2label = np.zeros(len(labels))
    cat3label = np.zeros(len(labels))
    cat4label = np.zeros(len(labels))
    cat5label = np.zeros(len(labels))
    cat6label = np.zeros(len(labels))
    cat1label[np.all(labels == constants.CAT1_ONEHOT) == 1] = 1
    cat2label[np.all(labels == constants.CAT2_ONEHOT) == 1] = 1
    cat3label[np.all(labels == constants.CAT3_ONEHOT) == 1] = 1
    cat4label[np.all(labels == constants.CAT4_ONEHOT) == 1] = 1
    cat5label[np.all(labels == constants.CAT5_ONEHOT) == 1] = 1
    cat6label[np.all(labels == constants.CAT6_ONEHOT) == 1] = 1

    #return as batch size to get normal distribution
    return inputs,labels,cat1label.reshape((n,1)),cat2label.reshape((n,1)),cat3label.reshape((n,1)),cat4label.reshape((n,1)),cat5label.reshape((n,1)),cat6label.reshape((n,1))

#gets n patches from an image with its respective label
def getBatch(n,catname='mixed'):
    cats = ['treematter','plywood','cardboard','bottles','trashbag','blackbag']
    random.seed(None)
    inputs = []
    labels = []

    #initialize var