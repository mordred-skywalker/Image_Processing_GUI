import cv2
import imutils
from matplotlib import pyplot as plt


class reader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_img(self):
        img = cv2.imread(self.filepath)
        plt.imshow(img)
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
            cv2.drawContours(img, [c], -1, (255, 255, 255), 2)
            cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        return img, coord


if __name__ == '__main__':

    test = reader('/Users/mordredyuan/Downloads/htcpID617_well02_P-21-11-10_stitch1_c4_1x_.tiff')
    img1, threshold = test.read_img()
    img2 = test.get_center(threshold)
    img3, coord = test.get_coord(img2, img1)
