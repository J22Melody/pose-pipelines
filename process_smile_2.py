import sys
from pathlib import Path

from pose_estimation_2 import pose_estimate


if len(sys.argv) < 2:
    print('Please specify the directory for Smile II!')
    exit()

data_path = sys.argv[1]
file_paths = Path(data_path).rglob('*.mp4')

for i, file_path in enumerate(file_paths):
    print('Processing file {} ...'.format(file_path))
    output = str(file_path).split('.')[0] + '.pose'
    pose_estimate(str(file_path), output, i == 0)