#!/bin/bash

directory=$1

for file in "$directory"*.mp4; do
    output="${file//.mp4/.pose}"
    python pose_estimation.py $file $output openpose
done
