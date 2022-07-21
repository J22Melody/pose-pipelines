import argparse
import json

import sys
from functools import lru_cache

import cv2
import os

import numpy as np
from draw import draw_pose

# Import OpenPose
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append('/openpose/build/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found.')
    print('Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


@lru_cache()
def get_hand_detector():
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/openpose/models/"
    params["hand"] = True
    params["hand_detector"] = 2
    params["body"] = 0

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    return opWrapper


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Point to a directory containing images and nothing else", required=True)
    parser.add_argument('-o', '--output', help='Point to a directory where you want the output to be saved',
                        required=True)
    parser.add_argument('-f', '--format', default='json', help='One of image/json')
    parser.add_argument('-d', '--device', default='gpu', help='One of cpu or gpu')
    args = parser.parse_args()

    files = os.listdir(args.input)
    print(files)

    if len(files) == 0:
        raise Exception("Input directory is empty")

    print("Found", len(files), "files")

    images = [cv2.imread(os.path.join(args.input, f)) for f in files]
    data = []
    for image in images:
        # Create new datum
        datum = op.Datum()
        datum.cvInputData = image
        datum.handRectangles = [
            # Left/Right hands person 0
            [
                op.Rectangle(0., 0., 0., 0.),
                op.Rectangle(0, 0, image.shape[0], image.shape[1]),
            ],
        ]
        data.append(datum)
        get_hand_detector().emplaceAndPop([datum])

    for f, image, datum in zip(files, images, data):
        pose = [[float(x) for x in r][:2] for r in np.array(datum.handKeypoints[1][0], dtype=np.float16)]
        print(pose)

        save_loc = os.path.join(args.output, f)
        if args.format == "json":
            json.dump(pose, open(save_loc + ".json", "w"))
        else:
            new_image = draw_pose(image, pose)
            cv2.imwrite(save_loc, new_image)
