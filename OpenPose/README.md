# OpenPose
Full body pose estimation with face and hands.

### Building from scratch:
```bash
docker build -t "openpose" .
```
Currently, the default entrypoint is `/bin/bash`.

### Running a container:
For input, we need to mount a video (`/video.mp4`), and optionally an output directory (`/out`).

```bash
nvidia-docker run -it --rm
    -v /home/nlp/amit/some_video.mp4:/video.mp4 
    openpose /bin/bash
```

### Running Pose Estimation
```bash
./build/examples/openpose/openpose.bin --video /video.mp4 --model_pose BODY_25 --display 0 --render_pose 0 --write_json /out/ --hand --face --num_gpu 1  --num_gpu_start 1
```
You can specify any option that exists in the openpose documentation.