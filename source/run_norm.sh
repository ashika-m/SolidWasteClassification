#!/bin/bash

CARDBOARD_DIR="trash_images/cardboard/ingroup/"
TREEMATTER_DIR="trash_images/treematter/ingroup/"
PLYWOOD_DIR="trash_images/plywood/ingroup/"
TRASHBAG_DIR="trash_images/trashbag/ingroup/"
BOTTLES_DIR="trash_images/bottles/ingroup/"
BLACKBAG_DIR="trash_images/blackbag/ingroup/"
GROUND_DIR="categories/ground/ingroup/"
MIXED_DIR="trash_images/mixed/ingroup/"
OUT_DIR1="normalized_bgrsegment_nobg"

mkdir $OUT_DIR1
echo "Start normalizing"
# echo "Normalizing Cardboard"
# python normalize.py normImage $CARDBOARD_DIR $OUT_DIR1 &
# echo "Normalizing Treematter"
# python normalize.py normImage $TREEMATTER_DIR $OUT_DIR1 &
# echo "Normalizing Plywood"
# python normalize.py normImage $PLYWOOD_DIR $OUT_DIR1 &
# echo "Normalizing Bottles"
# python normalize.py normImage $BOTTLES_DIR $OUT_DIR1 &
#echo "Normalizing Black Bag"
#python normalize.py normImage $BLACKBAG_DIR $OUT_DIR1 &
# echo "Normalizing Trash Bag"
# python normalize.py normImage $TRASHBAG_DIR $OUT_DIR1 &
echo "Normalizing Mixed"
python normalize.py normImage $MIXED_DIR $OUT_DIR1 &
wait

#python save_segments.py rotate $OUT_DIR1

echo "DONE normalizing"
