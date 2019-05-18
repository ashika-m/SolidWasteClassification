#!/bin/bash

CARDBOARD_DIR="categories/cardboard/ingroup/"
TREEMATTER_DIR="categories/treematter/ingroup/"
PLYWOOD_DIR="categories/plywood/ingroup/"
TRASHBAG_DIR="categories/trashbag/ingroup/"
BOTTLES_DIR="categories/bottles/ingroup/"
BLACKBAG_DIR="categories/blackbag/ingroup/"
GROUND_DIR="categories/ground/ingroup/"
MIXED_DIR="categories/mixed/"
OUT_DIR1="hsvsegmentation_bgrsegment_nobg"
OUT_DIR2="hsvsegmentation_bgrsegment_withbg"

mkdir $OUT_DIR1
echo "Start normalizing"
python normalize.py normImage $CARDBOARD_DIR $OUT_DIR1 &
python normalize.py normImage $TREEMATTER_DIR $OUT_DIR1 &
python normalize.py normImage $PLYWOOD_DIR $OUT_DIR1 &
python normalize.py normImage $BOTTLES_DIR $OUT_DIR1 &
python normalize.py normImage $BLACKBAG_DIR $OUT_DIR1 &
python normalize.py normImage $TRASHBAG_DIR $OUT_DIR1 &
wait

#python save_segments.py rotate $OUT_DIR1

echo "DONE normalizing"
