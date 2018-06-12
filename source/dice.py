
import cv2
import numpy as np
import os
import sys

names= ['treematter','plywood','cardboard','black bags','trash bags', 'plastic bottles']
treematter_mask = [0,0,255]
plywood_mask = [0,255,0]
cardboard_mask = [255,0,0]
blackbag_mask = [255,255,0]
trashbag_mask = [255,0,255]
bottles_mask = [0,255,255]
mask_colors = [treematter_mask,plywood_mask,cardboard_mask,blackbag_mask,trashbag_mask,bottles_mask]

def dice(img,gt,fout='dice_output.txt'):
    accs = []
    ratios = []
    with open(fout,'w') as fo:
        for cat,mask in zip(names,mask_colors):
            TP = float(np.count_nonzero(np.logical_and(np.all(img == mask,axis=2), np.all(gt == mask,axis=2))))
            TN = float(np.count_nonzero(np.logical_and(np.logical_not(np.all(img == mask,axis=2)), np.logical_not(np.all(gt == mask,axis=2)))))
            FP = float(np.count_nonzero(np.logical_and(np.all(img == mask,axis=2),np.logical_not(np.all(gt == mask,axis=2)))))
            FN = float(np.count_nonzero(np.logical_and(np.logical_not(np.all(img == mask,axis=2)),np.all(gt == mask,axis=2))))
            P = float(TP + FN)
            N = float(TN + FP)

            binary1 = np.array(np.all(img == mask,axis = 2),dtype=np.uint8)
            binary2 = np.array(np.all(gt == mask,axis = 2),dtype=np.uint8)
            b1_and_b2 = np.array(np.logical_and(binary1,binary2),dtype=np.uint8)
            binary1[binary1 == 1] = 255
            binary2[binary2 == 1] = 255
            b1_and_b2[b1_and_b2 == 1] = 255

            #for debugging purposes
            #cv2.imshow('binary1',cv2.resize(binary1,(500,500),interpolation=cv2.INTER_CUBIC))
            #cv2.imshow('binary2',cv2.resize(binary2,(500,500),interpolation=cv2.INTER_CUBIC))
            #cv2.imshow('b1_and_b2',cv2.resize(b1_and_b2,(500,500),interpolation=cv2.INTER_CUBIC))
            #cv2.waitKey(0)

            if (P+N) == 0:
                print('error with p + n')
            elif(P) == 0:
                print('error with p')
                P += 1
            elif(N) == 0:
                print('error with n')
                N += 1

            if (TP + FP) == 0:
                FP += 1

            PREC = (TP) / (TP + FP)
            ACC = (TP + TN) / (P + N)
            SENS= TP / P
            SPEC= TN / N

            DICE = TP / (P + FP)

            ratios.append(100 * np.count_nonzero(np.all(gt == mask,axis=2)) / (P + N))
            accs.append(DICE)

            print('-----category: %s ------' %cat)
            print('True Positive: %f' % TP)
            print('True Negative: %f' % TN)
            print('False Positive: %f' % FP)
            print('False Negative: %f' % FN)
            print('Positive: %f' % P)
            print('Negative: %f\n' % N)
            print('PRECICSION: %f' % PREC)
            print('ACCURACY: %f' % ACC)
            print('SENSITIVITY: %f' % SENS)
            print('SPECIFICITY: %f' % SPEC)
            print('ACCURACY: %f' % ACC)
            print('DICE: %f' % DICE)
            print('--------------')

            fo.write('--------' + cat + '--------\n\n\n')
            fo.write('True Positive: %f\n' % TP)
            fo.write('True Negative: %f\n' % TN)
            fo.write('False Positive: %f\n' % FP)
            fo.write('False Negative: %f\n' % FN)
            fo.write('Positive: %f\n' % P)
            fo.write('Negative: %f\n\n' % N)
            fo.write('PRECICSION: %f\n' % PREC)
            fo.write('SENSITIVITY: %f\n' % SENS)
            fo.write('SPECIFICITY: %f\n' % SPEC)
            fo.write('ACCURACY: %f\n' % ACC)
            fo.write('DICE: %f\n\n\n' % DICE)

        total_acc = 0
        for r,acc in zip(ratios,accs):
            total_acc += r * acc

            print('TOTAL ACCURACY: %f' % total_acc)
            fo.write('TOTAL ACCURACY: %f\n' % total_acc)
            fo.write('---------------------------------------------------\n')

    return total_acc,accs


#main function
if __name__ == '__main__':
    #maker sure of correct sys args
    if len(sys.argv) == 3:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]

        #check if directory exists then read the images
        if os.path.exists(dir1) and os.path.exists(dir2):
            img = cv2.imread(dir1,cv2.IMREAD_COLOR)
            gt = cv2.imread(dir2,cv2.IMREAD_COLOR)

            #output to results directory
            if not os.path.exists('results'):
                os.makedirs('results')

            #create file name
            fname = "RESULTS_" + str(os.path.splitext(os.path.basename(sys.argv[1]))[0]) + ".txt"
            fout = os.path.join('results',fname)

            #apply dice score calculation
            dice_score, cat_dice = dice(img,gt,fout)

        else:
            print("PATH DOES NOT EXIST: \n\t%s, \n\t%s" %(sys.argv[1],sys,argv[2]))
            sys.exit()
    else:
        print("wrong number of arguments")
        print("expecting 2")
