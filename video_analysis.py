import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from keyclipwriter import KeyClipWriter
import datetime


def make_cuts(filename, output_path, buff_size=64):
    output_vids = []
    # initialize key clip writer and the consecutive number of
    # frames that have *not* contained any action
    kcw = KeyClipWriter(buff_size)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    # fgbg = cv2.createBackgroundSubtractorMOG2()

    consec_frames = 0
    motion_timestamps = []

    vid = cv2.VideoCapture(filename)
    is_empty = True
    frame_count = 0
    while vid.isOpened():
        ret, image = vid.read()
        if image is None:
            break
        update_consec_frames = True
        small = imutils.resize(image, width=min(400, image.shape[1]))
        # fgmask = fgbg.apply(image)
        (rects, weights) = hog.detectMultiScale(small, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

        if len(rects) > 0:
            update_consec_frames = False
            consec_frames = 0

            # draw rectangles (on small)
            for (x, y, w, h) in rects:
                cv2.rectangle(small, (x, y), (x + w, y + h), (0, 0, 255), 2)

            if not kcw.recording:
                timestamp = datetime.datetime.now()
                p = "{}/{}.mp4".format(output_path,
                                       timestamp.strftime("%Y%m%d-%H%M%S"))
                # kcw.start(p, cv2.VideoWriter_fourcc(*'MJPG'), 30)
                kcw.start(p, cv2.VideoWriter_fourcc(*'mp4v'), 30)
                output_vids.append(p)
        else:
            update_consec_frames = True

        if update_consec_frames:
            consec_frames += 1
        kcw.update(image)
        if kcw.recording and consec_frames == buff_size:
            kcw.finish()

        # if len(rects) > 0 and is_empty:
        #     motion_timestamps.append(frame_count)
        #     is_empty = False
        # elif len(rects) > 0 and not is_empty:
        #     is_empty = False
        # elif len(rects) == 0 and not is_empty:
        #     motion_timestamps.append(frame_count)
        #     is_empty = True
        # else:
        #     is_empty = True

        cv2.imshow("final", small)

        frame_count += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            vid.release()
            break

    # TODO remove tiny clips

    if kcw.recording:
        kcw.finish()
    return output_vids


# print(make_cuts("clips/test2.mov", "output"))
# print(make_cuts("clips/test_cascade.mov"))

# TODO clip.duration -- (frames/total_frames)*duration
