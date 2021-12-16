from PIL import Image
import cv2
import imutils


class reader:
    '''
    This class acts as an initializer for the reader class that will take in
    a filepath as user input and perform subsequent functions to read in the
    image, convert the image accordingly, get the centers for the cells in
    the image, and get these center points' coordinates as a list of tuples
    while also returning the processed and annotated image as output. Some of
    the code was adapted from a tutorial website on opencv usage.
    (https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/)

    '''
    def __init__(self, filepath):
        self.filepath = filepath

    def read_img(self):
        '''
        This will read a image using the filepath provided, convert it to
        grayscale, apply a Gaussian filter to the image, apply thresholding,
        and return the original and processed image as two arrays.

        **Parameters**

            None

        **Returns**

            img: *list, list, int*
                A 2D array that represents the original input image.
            processed: *list, list, int*
                A 2D array that represents the processed image.
        '''

        # load the image
        img = cv2.imread(self.filepath)
        # convert the image to grayscale
        grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # apply a Gaussian filter to the image
        after_filter = cv2.GaussianBlur(grayscale, (3, 3), 0)
        # convert the image to binary by applying thresholding
        processed = cv2.threshold(after_filter, 20, 255, cv2.THRESH_BINARY)[1]
        return img, processed

    def get_center(self, processed):
        '''
        This will find the contours and the according centers for all the
        cells shown in the image.

        **Parameters**

            processed: *list, list, int*
                A 2D array that represents the processed image.

        **Returns**

            centers: *list, list, int*
                A 2D array that represents the thresholded image.
        '''
        # use opencv to find contours in the processed image
        centers = cv2.findContours(processed.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        centers = imutils.grab_contours(centers)
        return centers

    def get_coord(self, centers, img):
        '''
        This will find the contours and the according centers for all the
        cells shown in the image.

        **Parameters**

            img: *list, list, int*
                A 2D array that represents the processed image.
            centers: *list, list, int*
                A 2D array that represents the thresholded image.

        **Returns**

            img: *list, list, int*
                A 2D array that represents the annotated image.
            coord: *list, list, tup*
                A list of coordinates of the centers of the cells
                as tuples.
        '''
        # loop over the contours
        coord = []
        for c in centers:
            # compute the center of the contour
            M = cv2.moments(c)
            # take into consideration when M["m00"] is 0
            # calculate the coordinates of the centers
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                coord.append((cX, cY))
            else:
                # set coordinates to 0 if M["m00"] is 0
                cX, cY = 0, 0

            # annotate the contour and the center of the cells on the image
            cv2.drawContours(img, [c], -1, (255, 255, 255), 1)
            cv2.circle(img, (cX, cY), 1, (0, 255, 0), -1)
            # put the coordinates onto the image
            cv2.putText(img, '{cd}'.format(cd=(cX, cY)), (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.25, (255, 255, 255), 1)
        return img, coord


def img_process(filepath):
    '''
    This function takes in the filepath and create a reader class instance.
    The original image will then be runned through a series of pipelines to
    return the final annotated image and a list of center points' coordinates.
    '''
    test = reader(filepath)
    img1, threshold = test.read_img()
    img2 = test.get_center(threshold)
    img3, coord = test.get_coord(img2, img1)
    return img3, coord


def show_cropped_image(img, x, y, size):
    '''
    This function will crop the input image according to coordinates and
    final image size. The output image should contain enlarged cell views.

    **Parameters**

        img: *list, list, int*
            A 2D array that represents the annotated image.
        x: *int*
            The x coordinate of the center point.
        y: *int*
            The y coordinate of the center point.
        size: *int*
            The size of the generated output image.

    **Returns**

        new_img: *list, list, int*
            A 2D array that represents the cropped image.

    '''
    # calculate the upper left coordinates and the lower right coordinates
    left = x - size // 2
    top = y - size // 2
    right = x + size // 2
    bottom = y + size // 2

    # transform the image and use the coordinates to crop the image
    im_transform = Image.fromarray(img)
    new_img = im_transform.crop((left, top, right, bottom))
    new_img = new_img.save('new_img.jpg')

    return new_img
