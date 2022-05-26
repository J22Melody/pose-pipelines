import sys
import cv2
import numpy as np

import mediapipe as mp
from pose_format import Pose
from pose_format.utils.holistic import load_holistic
from pose_format.pose_visualizer import PoseVisualizer

mp_holistic = mp.solutions.holistic
FACEMESH_CONTOURS_POINTS = [str(p) for p in sorted(set([p for p_tup in list(mp_holistic.FACEMESH_CONTOURS) for p in p_tup]))]


def load_video_frames(cap: cv2.VideoCapture):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cap.release()

def pose_visualize(pose, output, video_path):
    p = pose.get_components(["POSE_LANDMARKS", "FACE_LANDMARKS", "LEFT_HAND_LANDMARKS", "RIGHT_HAND_LANDMARKS"], 
        {"FACE_LANDMARKS": FACEMESH_CONTOURS_POINTS})
    print(p.body.data.shape)
    v = PoseVisualizer(p, thickness=1)
    v.save_video("{}.mp4".format(output), v.draw())
    v.save_video("{}.overlay.mp4".format(output), v.draw_on_video(video_path))

def pose_estimate(path, output, visualize=False):
    # # Load video frames
    # cap = cv2.VideoCapture(path)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # frames = load_video_frames(cap)
    # video_metadata = dict(fps=fps, width=width, height=height)
    # print(video_metadata)

    # # Perform pose estimation
    # pose = load_holistic(frames, fps=fps, width=width, height=height, depth=width, progress=True, 
    #     additional_holistic_config={'model_complexity': 2, 'refine_face_landmarks': True})

    # # Write 
    # with open(output, "wb") as f:
    #     pose.write(f)

    # Read
    with open(output, "rb") as f:
        buffer = f.read()
        pose = Pose.read(buffer)

    print(pose.body.data.shape)

    # Visualize
    if visualize:
        pose_visualize(pose, output, path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Please specify the path for the video and the output!')
        exit()

    path = sys.argv[1]
    output = sys.argv[2]

    pose_estimate(path, output, visualize=True)