import sys
import cv2
import numpy as np

from pose_format import Pose
from pose_format.utils.holistic import load_holistic
from pose_format.pose_visualizer import PoseVisualizer


if len(sys.argv) < 3:
    print('Please specify the path for the video and the output!')
    exit()

path = sys.argv[1]
output = sys.argv[2]

def load_video_frames(cap: cv2.VideoCapture):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()

# Load video frames
cap = cv2.VideoCapture(path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frames = load_video_frames(cap)
video_metadata = dict(fps=fps, width=width, height=height)
print(video_metadata)

# Perform pose estimation
pose = load_holistic(frames, fps=fps, width=width, height=height, depth=width, progress=True, 
    model_complexity=2, refine_face_landmarks=True)

# Write 
with open(output, "wb") as f:
  pose.write(f)

# Read
with open(output, "rb") as f:
  buffer = f.read()
  pose = Pose.read(buffer)

print(vars(pose))
print(vars(pose.header))
print(pose.body.data.shape)

# Visualize
v = PoseVisualizer(pose, thickness=1)
v.save_video("pose.mp4", v.draw(max_frames=3000))
v.save_video("pose_on_video.mp4", v.draw_on_video(path, max_frames=3000))