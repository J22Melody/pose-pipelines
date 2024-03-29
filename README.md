# pose-pipelines

Pipelines to process (crop, mask, and estimate poses) sign language videos like the way described in WMT-SLT 22: 

https://www.wmt-slt.com/data#h.23ktnxrb3yhc

### Requirements

Python 3.8.11 (a virtual Python environment is recommended)

Install MediaPipe:
https://google.github.io/mediapipe/getting_started/python.html

Install other dependencies:

`pip install pose-format` (the library we use to store `.pose` files) 

`pip install vidgear`

### Example Video Files

- example.mp4: already cropped and masked video
- example_2.mp4: raw video from TV show

### Cropping

`python cropping.py example_2.mp4 example_2.cropped.mp4 100 0 400 1000`

### Masking

`python masking.py example_2.cropped.mp4 example_2.cropped.masked.mp4`

### Pose Estimation By Mediapipe Holistic (on CPU)

`python pose_estimation.py example.mp4 example.mediapipe.pose mediapipe`

### Pose Estimation By Openpose (on GPU)

Pose estimation by Openpose requires a specific environment setup that is more complicated than simply installing and calling a Python library.

We offer a container solution (on S3IT):

`cd ~/data/`

`singularity pull docker://cwaffles/openpose`

`singularity build --sandbox openpose_latest openpose_latest.sif`

`sbatch ./job_openpose.sh`

Finally, read the Openpose output files and write them to a `.pose` file:

`python pose_estimation.py example.mp4 example.openpose.pose openpose`

### Links

- Example Pose Format:
    - https://colab.research.google.com/drive/1-KVOmJalbmKzpZYST2qnEZ7L3J9uj8uR?usp=sharing
    - https://colab.research.google.com/drive/14FWXViVTYEIRFb4s9TpNXRiIJ6Xtfykc?usp=sharing
- MediaPipe Holistic:
https://google.github.io/mediapipe/solutions/holistic.html
- Openpose:
https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_installation_0_index.html

### Citation

```
@misc{jiang2022pose-pipelines, 
    title={pose-pipelines: Pipelines to process sign language videos like the way described in WMT-SLT 22},
    author={Jiang, Zifan},
    howpublished={\url{https://github.com/J22Melody/pose-pipelines}},
    year={2022}
}
```
