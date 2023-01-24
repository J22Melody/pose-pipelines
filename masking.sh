#!/bin/bash

directory=$1

for file in "$directory"*.cropped.mp4; do
    output="${file//.mp4/.masked.mp4}"
    # echo "$output"
    python masking.py $file $output
done