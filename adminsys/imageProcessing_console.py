import cv2 as cv
from pathlib import Path
import os
from django.conf import settings
import matplotlib.pyplot as plt
from django.conf import settings


def customizeMockup(path, savepath):

    img = cv.imread(path)
    mockup1 = cv.imread(f"{settings.MEDIA_ROOT}/ps5-left.png")

    mockup2 = cv.imread(f"{settings.MEDIA_ROOT}/ps5-right.png")

    mask1 = cv.inRange(mockup1, (0, 0, 0), (200, 100, 100))
    mask2 = cv.inRange(mockup2, (0, 0, 0), (200, 100, 100))
    l1, w1 = mask1.shape
    l2, w2 = mask2.shape
    img_out1 = cv.resize(img, (w1, l1))
    img_out2 = cv.resize(img, (w2, l2))
    img_out1 = cv.bitwise_and(img_out1, img_out1, mask=mask1)
    img_out2 = cv.bitwise_and(img_out2, img_out2, mask=mask2)

    cv.imwrite(
        savepath+"_console_l.png", img_out1)
    cv.imwrite(
        savepath+"_console_r.png", img_out2)
    # mask1 = np.reshape(mask1, [w,l,3])
    return img_out1, img_out2
