import sys
import numpy as np
import cv2
from vidgear.gears import WriteGear


def crop_video(video_path, output_path, x=0, y=0, w=1024, h=1024):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Initialize frame counter
    cnt = 0

    # Some characteristics from the original video
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    output_params = {
      "-vcodec": "libx264",
      "-crf": 18,
      "-preset": "fast",
      "-input_framerate": fps,
      "-pix_fmt": "yuv420p",
    }

    # Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
    out = WriteGear(output_filename=output_path, logging=False, custom_ffmpeg=None, **output_params)


    # Now we start
    while(cap.isOpened()):
        ret, frame = cap.read()

        cnt += 1 # Counting frames

        # Avoid problems when video finish
        if ret:
            # Croping the frame
            crop_frame = frame[y:y+h, x:x+w]

            # Percentage
            if cnt % 100 == 0:
                xx = cnt *100/frames
                print(int(xx),'%')

            # Saving from the desired frames
            #if 15 <= cnt <= 90:
            #    out.write(crop_frame)

            # I see the answer now. Here you save all the video
            out.write(crop_frame)

            # Just to see the video in real time          
            # cv2.imshow('frame',frame)
            # cv2.imshow('croped',crop_frame)
        else:
            break

    cap.release()
    out.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please specify the video_path for the video and the output_path!')
        exit()

    video_path = sys.argv[1]
    output_path = sys.argv[2]

    if len(sys.argv) > 6:
        x = int(sys.argv[3])
        y = int(sys.argv[4])
        w = int(sys.argv[5])
        h = int(sys.argv[6])
        crop_video(video_path, output_path, x, y, w, h)
    else:
        crop_video(video_path, output_path)