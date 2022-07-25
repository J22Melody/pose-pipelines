# pose-pipelines

### Requirements

Install MediaPipe:
https://google.github.io/mediapipe/getting_started/python.html

Install other dependencies:
`pip install pose-format`

### Cropping

`python cropping.py example_2.mp4 example_2.cropped.mp4`

### Masking

`python masking.py example_2.cropped.mp4 example_2.cropped.masked.mp4`

### Pose estimation

By Mediapipe Holistic

`python pose_estimation.py example_2.cropped.masked.mp4 example_2.mediapipe.pose`

By Openpose

TODO

### Links

- Example Pose Format:
    - https://colab.research.google.com/drive/1-KVOmJalbmKzpZYST2qnEZ7L3J9uj8uR?usp=sharing
    - https://colab.research.google.com/drive/14FWXViVTYEIRFb4s9TpNXRiIJ6Xtfykc?usp=sharing
- MediaPipe Holistic:
https://google.github.io/mediapipe/solutions/holistic.html
