import sys
import numpy as np
import cv2
from vidgear.gears import WriteGear

def crop_video(video_path, output_path, x=100, y=0, h=1024, w=1024):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Initialize frame counter
    cnt = 0

    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Here you can define your croping values
    # x,y,h,w = 0,0,720,640

    # output
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

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
        if ret==True:
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

    crop_video(video_path, output_path)