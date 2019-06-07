#!/bin/bash

CARDBOARD_DIR="categories/cardboard_comp_norm/"
TREEMATTER_DIR="categories/treematter_comp_norm/"
PLYWOOD_DIR="categories/plywood_comp_norm/"
TRASHBAG_DIR="categories/trashbag_comp_norm/"
BOTTLES_DIR="categories/bottles_comp_norm/"
BLACKBAG_DIR="categories/blackbag_comp_norm/"
MIXED_DIR="categories/mixed_comp_norm/"
GROUND_DIR="categories/mixed/gt/"
OUT_DIR1="bgrsegmentation_nobg"

mkdir $OUT_DIR1
python save_segments.py save $CARDBOARD_DIR $OUT_DIR1 &
python save_segments.py save $TREEMATTER_DIR $OUT_DIR1 &
python save_segments.py save $PLYWOOD_DIR $OUT_DIR1 &
python save_segments.py save $BOTTLES_DIR $OUT_DIR1 &
python save_segments.py save $BLACKBAG_DIR $OUT_DIR1 &
python save_segments.py save $TRASHBAG_DIR $OUT_DIR1 &
python save_segments.py save $MIXED_DIR $OUT_DIR1 &
python save_segments.py save $GROUND_DIR $OUT_DIR1 &
wait

python save_segments.py rotate $OUT_DIR1

echo "Done extracting blobs"
