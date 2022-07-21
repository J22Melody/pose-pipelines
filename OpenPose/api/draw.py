import math

import cv2
import numpy as np

JOINTS = 21

joint_color_code = [[0, 0, 192],
                    [0, 192, 192],
                    [0, 192, 0],
                    [192, 192, 0],
                    [192, 0, 0],
                    [127, 127, 127]]

limbs = [[0, 1],
         [1, 2],
         [2, 3],
         [3, 4],
         [0, 5],
         [5, 6],
         [6, 7],
         [7, 8],
         [0, 9],
         [9, 10],
         [10, 11],
         [11, 12],
         [0, 13],
         [13, 14],
         [14, 15],
         [15, 16],
         [0, 17],
         [17, 18],
         [18, 19],
         [19, 20]]


def draw_pose(image, joints, RGB=True):
    image = image.copy()

    joints = [(int(x), int(y)) for x, y in joints]

    for i, joint in enumerate(joints):
        j = i - 1
        color_code_num = (j // 4)

        color = [x + 35 * (j % 4) for x in joint_color_code[color_code_num]]
        if not RGB:
            color = list(reversed(color))

        cv2.circle(image, center=joint, radius=3, color=color, thickness=-1)

    for i, (j1, j2) in enumerate(limbs):
        color_code_num = (i // 4)
        color = [x + 35 * (i % 4) for x in joint_color_code[color_code_num]]
        if not RGB:
            color = list(reversed(color))

        jo1 = joints[j1]
        jo2 = joints[j2]
        length = math.hypot(jo1[0] - jo2[0], jo1[1] - jo2[1])

        deg = math.degrees(math.atan2(jo1[0] - jo2[0], jo1[1] - jo2[1]))
        polygon = cv2.ellipse2Poly((int((jo1[0] + jo2[0]) / 2), int((jo1[1] + jo2[1]) / 2)),
                                   (int(length / 2), 3),
                                   90 - int(deg), 0, 360, 1)

        cv2.fillConvexPoly(image, polygon, color=color)

    return image


if __name__ == "__main__":
    pass
