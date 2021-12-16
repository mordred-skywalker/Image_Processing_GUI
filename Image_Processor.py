import PIL
from PIL import Image
import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt


class reader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_img(self):
        img = cv2.imread(self.filepath)
        # plt.imshow(img)
        # load the image, convert it to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)[1]
        return img, thresh

    def get_center(self, thresh):
        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        return cnts

    def get_coord(self, cnts, img):
        # loop over the contours
        coord = []
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                coord.append((cX, cY))
            else:
                # set values as what you need in the situation
                cX, cY = 0, 0

            # draw the contour and center of the shape on the image
            cv2.drawContours(img, [c], -1, (255, 255, 255), 1)
            cv2.circle(img, (cX, cY), 1, (0, 255, 0), -1)
            cv2.putText(img, '{cd}'.format(cd=(cX, cY)), (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.25, (255, 255, 255), 1)
        return img, coord


def img_process(filepath):
    test = reader(filepath)
    img1, threshold = test.read_img()
    img2 = test.get_center(threshold)
    img3, coord = test.get_coord(img2, img1)
    return img3, coord


def show_cropped_image(img, x, y, size):
    left = x - size / 2
    top = y - 50
    right = x + 50
    bottom = y + 50

    im_transform = Image.fromarray(img)
    new_img = im_transform.crop((left, top, right, bottom))
    new_img = new_img.save('new_img.jpg')

    return new_img


if __name__ == '__main__':

    img, coord = img_process('/Users/mordredyuan/Downloads/htcpID617_well02_P-21-11-10_stitch1_c4_1x_.tiff')

    show_cropped_image(img, coord[1][0], coord[1][1], 100)
