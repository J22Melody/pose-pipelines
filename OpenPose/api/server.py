# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import json
from flask import Flask, request, jsonify
import base64
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Import OpenPose
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append('/openpose/build/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found.')
    print('Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/openpose/models/"
params["face"] = True
params["hand"] = True

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


@app.route('/', methods=['POST'])
def main():
    img_base64 = request.data.decode("utf-8")
    print("img_base64", img_base64)

    data_base64 = img_base64.split(",")[1]

    decoded_data = base64.b64decode(data_base64)

    img = cv2.cvtColor(np.array(Image.open(BytesIO(decoded_data))), cv2.COLOR_BGR2RGB)

    datum = op.Datum()

    datum.cvInputData = img
    opWrapper.emplaceAndPop([datum])

    pose = [
        {
            "people": [
                {
                    "pose_keypoints_2d": datum.poseKeypoints.flatten().tolist(),
                    "face_keypoints_2d": datum.faceKeypoints.flatten().tolist(),
                    "hand_left_keypoints_2d": datum.handKeypoints[0].flatten().tolist(),
                    "hand_right_keypoints_2d": datum.handKeypoints[1].flatten().tolist(),
                }
            ]
        }
    ]

    return jsonify(pose)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8485)
