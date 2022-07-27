import sys
from pathlib import Path

from pose_estimation import pose_estimate


if len(sys.argv) < 2:
    print('Please specify the directory for videos to estimate!')
    exit()

data_path = sys.argv[1]
file_paths = Path(data_path).rglob('*.mp4')
file_paths = [str(f) for f in file_paths if '.pose.' not in str(f)]

for i, file_path in enumerate(file_paths):
    print('Processing file {} ...'.format(file_path))
    prefix_name = '.'.join(file_path.split('.')[:-1])
    output = prefix_name + '.pose'
    pose_estimate(file_path, output, True, True)