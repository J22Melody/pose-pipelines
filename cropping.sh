#!/bin/bash

directory=$1

for file in "$directory"/*.mp4; do
    output="${file//.mp4/.cropped.mp4}"
    # echo "$output"
    python cropping.py $file $output
done