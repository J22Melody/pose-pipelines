import cv2
import sys
import mediapipe as mp
import numpy as np
from typing import Iterator
from tqdm import tqdm
from vidgear.gears import WriteGear

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation


BG_COLOR = (192, 192, 192) # gray

def save_video(f_name: str, frames: Iterator, custom_ffmpeg=None):
    # image_size = (self.pose.header.dimensions.width, self.pose.header.dimensions.height)

    output_params = {
      "-vcodec": "libx264",
      "-crf": 0,
      "-preset": "fast",
      "-input_framerate": 25,
    }

    # Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
    out = WriteGear(output_filename=f_name, logging=False, custom_ffmpeg=custom_ffmpeg, **output_params)
    # out = cv2.VideoWriter(f_name, cv2.VideoWriter_fourcc(*'MP4V'), self.pose.body.fps, image_size)
    for frame in tqdm(frames):
      out.write(frame)

    out.close()

def mask_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    output_images = []
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=0) as selfie_segmentation:
        bg_image = None
        while True:
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = selfie_segmentation.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw selfie segmentation on the background image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.05
            # The background can be customized.
            #   a) Load an image (with the same width and height of the input image) to
            #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
            #   b) Blur the input image by applying image filtering, e.g.,
            #      bg_image = cv2.GaussianBlur(image,(55,55),0)
            if bg_image is None:
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR
            output_image = np.where(condition, image, bg_image)

            output_images.append(output_image)

    cap.release()

    save_video(output_path, output_images)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please specify the video_path for the video and the output_path!')
        exit()

    video_path = sys.argv[1]
    output_path = sys.argv[2]

    mask_video(video_path, output_path)