import cv2 as cv
import os


def customizeMockup(path):
    img = cv.imread(path)
    mockup1 = cv.imread(os.path.abspath('media/lap-back.png'))
    mockup2 = cv.imread(os.path.abspath('media/lap-keyboard2.png'))
    mask1 = cv.inRange(mockup1, (0, 0, 0), (200, 100, 100))
    mask2 = cv.inRange(mockup2, (0, 0, 0), (200, 100, 100))
    l1, w1 = mask1.shape
    l2, w2 = mask2.shape
    img_out1 = cv.resize(img, (w1, l1))
    img_out2 = cv.resize(img, (w2, l2))
    # mask1 = np.reshape(mask1, [w,l,3])
    return img_out1, img_out2


customizeMockup('back_3.jpg')
