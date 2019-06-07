

KEEP_RATE = 0.8                     #Rate of dropping out in the dropout layer
LOG_DIR = "../ops_logs"             #Directory where the logs would be stored for visualization of the training

#Neural network constants
cat1_dir = "../trash_images/treematter_normalized/"
cat2_dir = "../trash_images/plywood_normalized/"
cat3_dir = "../trash_images/cardboard_normalized/"
cat4_dir = "../trash_images/bottles_normalized/"
cat5_dir = "../trash_images/trashbag_normalized/"
cat6_dir = "../trash_images/blackbag_normalized/"
MIXEDFILE = "../trash_images/mixed_normalized/mixed14.png"
GROUND_TRUTH = "../trash_images/mixed/gt/mixed14_gt.png"
CAT1            = "treematter"
CAT2            = "plywood"
CAT3            = "cardboard"
CAT4            = "bottles"
CAT5            = "trashbag"
CAT6            = "blackbag"
CAT1_ONEHOT     = [1,0,0,0,0,0]
CAT2_ONEHOT     = [0,1,0,0,0,0]
CAT3_ONEHOT     = [0,0,1,0,0,0]
CAT4_ONEHOT     = [0,0,0,1,0,0]
CAT5_ONEHOT     = [0,0,0,0,1,0]
CAT6_ONEHOT     = [0,0,0,0,0,1]
LEARNING_RATE = 0.001               #Learning rate for training the CNN
CNN_LOCAL1 = 32                  #Number of features output for conv layer 1
CNN_GLOBAL = 32                  #Number of features output for conv layer 1
CLASSES      = 6
CNN_EPOCHS       = 3000
CNN_FULL   = 200                #Number of features output for fully connected layer1
FULL_IMGSIZE = 500
IMG_SIZE = 28
IMG_DEPTH   = 3
BATCH_SIZE = 300

MIN_DENSITY = 10000
SPATIAL_RADIUS = 5
RANGE_RADIUS = 5


