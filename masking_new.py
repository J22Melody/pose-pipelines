import cv2
import sys
import numpy as np
from typing import Iterator
from tqdm import tqdm
from vidgear.gears import WriteGear

BG_COLOR = (192, 192, 192) # gray

def mask_video(video_path, output_path, mask_path):
    
    cap = cv2.VideoCapture(video_path)
    cap_mask = cv2.VideoCapture(mask_path)
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    output_params = {
      "-vcodec": "libx264",
      "-crf": 18,
      "-preset": "fast",
      "-input_framerate": fps,
      "-pix_fmt": "yuv420p",
    }
    out = WriteGear(output=output_path, logging=False, custom_ffmpeg=None, **output_params)

    bg_image = None
    while True:
        success, image = cap.read()
        success_mask, image_mask = cap_mask.read()

        if not success or not success_mask:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            break

        if bg_image is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
        output_image = np.where(image_mask, image, bg_image)

        out.write(output_image)

    out.close()
    cap.release()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Please specify the video_path for the video and the output_path!')
        exit()

    video_path = sys.argv[1]
    output_path = sys.argv[2]
    mask_path = sys.argv[3]

    mask_video(video_path, output_path, mask_path)