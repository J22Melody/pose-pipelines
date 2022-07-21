# pose-pipelines

### Requirements

Install MediaPipe:
https://google.github.io/mediapipe/getting_started/python.html

Install other dependencies:
`pip install pose-format`

### Cropping

### Masking

### Pose estimation

Apart from OpenPose and Holistic, Monocular Total Capture (Xiang et al., 2018) and FrankMoCap (Rong et al., 2021) may also be alternatives. Our colleagues at Surrey ultimately trained a HRNet (J. Wang et al., 2020) model and fine-tuned it on sign language data. 

`python pose_estimation.py example.mp4 example.pose`

### Links

- Example Pose Format:
https://colab.research.google.com/drive/1-KVOmJalbmKzpZYST2qnEZ7L3J9uj8uR?usp=sharing
https://colab.research.google.com/drive/14FWXViVTYEIRFb4s9TpNXRiIJ6Xtfykc?usp=sharing
- MediaPipe Holistic:
https://google.github.io/mediapipe/solutions/holistic.html
