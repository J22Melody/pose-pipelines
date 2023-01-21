#!/bin/bash

directory=$1

for file in "$directory"*.mp4; do
    output="${file//.mp4/.openpose\/}"
    echo "$output"
    sbatch ./job_openpose.sh $file $output
done