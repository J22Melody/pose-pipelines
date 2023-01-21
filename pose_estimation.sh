#!/bin/bash

directory=$1

for file in "$directory"/*.cropped.masked.mp4; do
    output="${file//.mp4/.pose}"
    python pose_estimation.py $file $output
done

# for file in "$directory"/*.cropped.masked.mp4; do
#     output="${file//.mp4/.reduced.pose}"
#     python pose_estimation.py $file $output
# done