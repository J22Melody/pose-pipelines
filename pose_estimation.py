import sys
import cv2
import numpy as np

import mediapipe as mp
from pose_format import Pose
from pose_format.utils.holistic import load_holistic
from pose_format.utils.openpose import load_openpose_directory
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

def pose_estimate(video_path, output_path, lib='mediapipe', reduce=False):
    # Load video frames
    print('Load video ...')
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    frames = load_video_frames(cap)
    video_metadata = dict(fps=fps, width=width, height=height)
    print(video_metadata)

    # Perform pose estimation
    print('Estimating pose ...')

    if lib == 'mediapipe':
        pose = load_holistic(frames, fps=fps, width=width, height=height, progress=True, 
            additional_holistic_config={'model_complexity': 2, 'refine_face_landmarks': True})

        # Remove world landmarks by default
        pose = pose.get_components(["POSE_LANDMARKS", "FACE_LANDMARKS", "LEFT_HAND_LANDMARKS", "RIGHT_HAND_LANDMARKS"])

        # Reduce as Surrey did
        if reduce:
            pose = pose.get_components(["POSE_LANDMARKS", "FACE_LANDMARKS", "LEFT_HAND_LANDMARKS", "RIGHT_HAND_LANDMARKS"], 
                {"FACE_LANDMARKS": FACEMESH_CONTOURS_POINTS})
    elif lib == 'openpose':
        pose = load_openpose_directory(video_path.replace('.mp4', '.openpose'), fps=fps, width=width, height=height)

    print('Points:', pose.body.data.shape)

    # Write 
    print('Writing ...')
    with open(output_path, "wb") as f:
        pose.write(f)

def pose_visualize(video_path, pose_path, overlay=False):
    # Read
    print('Reading ...')
    with open(pose_path, "rb") as f:
        buffer = f.read()
        pose = Pose.read(buffer)

    # Visualize
    v = PoseVisualizer(pose, thickness=1)

    # Write
    if overlay:
        v.save_video("{}.overlay.mp4".format(pose_path), v.draw_on_video(video_path))
    else:
        v.save_video("{}.mp4".format(pose_path), v.draw())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Please specify the video_path for the video and the output_path!')
        exit()

    video_path = sys.argv[1]
    output_path = sys.argv[2]
    lib = sys.argv[3] if len(sys.argv) > 3 else 'mediapipe'

    pose_estimate(video_path, output_path, reduce=True, lib=lib)
    pose_visualize(video_path, output_path, overlay=True)
    pose_visualize(video_path, output_path, overlay=False)