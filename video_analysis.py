import cv2
import numpy as np
import imutils

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def get_cuts(filename):
    motion_timestamps = []

    vid = cv2.VideoCapture(filename)
    is_empty = True
    frame_count = 0
    while vid.isOpened():
        ret, image = vid.read()
        if image is None:
            break
        image = imutils.resize(image, width=min(400, image.shape[1]))

        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)
        if len(rects) > 0 and is_empty:
            motion_timestamps.append(frame_count)
            is_empty = False
        elif len(rects) > 0 and not is_empty:
            is_empty = False
        elif len(rects) == 0 and not is_empty:
            motion_timestamps.append(frame_count)
            is_empty = True
        else:
            is_empty = True

        for (x, y, w, h) in rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("final", image)

        frame_count += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            vid.release()
            break

    # TODO support multiple highlights in one clip
    # count = 0
    # while count < len(motion_timestamps)-1:
    #     if (motion_timestamps[count+1] - motion_timestamps[count]) < 120:
    #         motion_timestamps.pop(count+1)
    #         count += 1

    return motion_timestamps
    # return [motion_timestamps[0], motion_timestamps[-1]]


# print(get_cuts("clips/test2.mov"))
print(get_cuts("clips/test_cascade.mov"))
