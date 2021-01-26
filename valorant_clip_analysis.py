import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from keyclipwriter import KeyClipWriter
import datetime
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


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
        height = 720
        width = 1280
        small = cv2.resize(image, (width, height))
        (rects, weights) = hog.detectMultiScale(small, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

        # Kill feed OCR
        # kfeed = cv2.rectangle(small, (int(width*0.725), int(height*0.08)), (int(width*0.9975), int(height*0.177777778)), (255, 255, 0))
        # roi = (849, 58, 424, 265)
        roi = (976, 70, 85, 17)
        kfeed = small[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        gray = cv2.bitwise_not(cv2.cvtColor(kfeed, cv2.COLOR_BGR2GRAY))
        # kfeed_roi = kfeed[int(width*0.725):int(width*0.9975), int(height*0.08):int(height*0.177777778)]
        # gray = cv2.cvtColor(kfeed, cv2.COLOR_BGR2GRAY)
        cv2.imshow("kfeed", gray)
        text = pytesseract.image_to_string(gray)
        print(text)

        # recording condition
        # if len(rects) > 0:
        #     update_consec_frames = False
        #     consec_frames = 0
        #
        #     # draw rectangles (on small)
        #     for (x, y, w, h) in rects:
        #         cv2.rectangle(small, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #
        #     if not kcw.recording:
        #         timestamp = datetime.datetime.now()
        #         p = "{}/{}.mp4".format(output_path,
        #                                timestamp.strftime("%Y%m%d-%H%M%S"))
        #         # kcw.start(p, cv2.VideoWriter_fourcc(*'MJPG'), 30)
        #         kcw.start(p, cv2.VideoWriter_fourcc(*'mp4v'), 30)
        #         output_vids.append(p)
        # else:
        #     update_consec_frames = True
        #
        # if update_consec_frames:
        #     consec_frames += 1
        # kcw.update(image)
        # if kcw.recording and consec_frames == buff_size:
        #     kcw.finish()

        # cv2.imshow("final", small)

        frame_count += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            vid.release()
            break

    # TODO remove tiny clips

    if kcw.recording:
        kcw.finish()
    return output_vids


print(make_cuts("input/valorant_clips/sheriff2.mp4", "valorant_analyzed"))
# print(make_cuts("clips/test_cascade.mov"))
