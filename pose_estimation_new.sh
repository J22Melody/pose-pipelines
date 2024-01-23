#!/bin/bash

input_directory=$1
output_directory=$2

mkdir -p $output_directory

for fullfile in "$input_directory"*.mp4; do
    filename=$(basename -- "$fullfile")
    filename="${filename%.*}"

    output="$output_directory/$filename.pose"

    if [ -e "$output" ]
    then
        echo "$output exists, skipping ..."
    else
        echo "video_to_pose -i $fullfile --format mediapipe -o $output"
        video_to_pose -i "$fullfile" --format mediapipe -o "$output"
    fi
done
