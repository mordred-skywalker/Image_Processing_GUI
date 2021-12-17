import io
import PySimpleGUIQt as sg
import os.path
import pandas as pd
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import imutils
from PIL import ImageFile

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True


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
            #cv2.drawContours(img, [c], -1, (255, 255, 255), 1)
            #cv2.circle(img, (cX, cY), 1, (0, 255, 0), -1)
            #cv2.putText(img, '{cd}'.format(cd=(cX, cY)), (cX - 20, cY - 20),
                        #cv2.FONT_HERSHEY_TRIPLEX, 0.25, (255, 255, 255), 1)
        return img, coord


def img_process(filepath):
    test = reader(filepath)
    img1, threshold = test.read_img()
    img2 = test.get_center(threshold)
    img3, coord = test.get_coord(img2, img1)
    return img3, coord


def show_cropped_image(img, x, y, size):
    left = int(x - size / 2)
    top = int(y - size / 2)
    right = int(x + size / 2)
    bottom = int(y + size / 2)

    im_transform = Image.fromarray(img)
    new_img = im_transform.crop((left, top, right, bottom))
    new_img = new_img.save('new_img.tif')

    return new_img


def main():
    file_types = [("TIFF(*.tif)", "*.tif")]   # specify file types to read
    Cellidx = []       # create cell index

    # Create column UI elements
    file_list_column = [
        [

            sg.Text("C1 Image Path:", size=(20, 1)),  # Text line
            sg.Input(size=(30, 1), enable_events=True, key="-C1FILE-"),     # Input File path
            sg.FileBrowse(file_types=file_types, size=(10, 1)),     # open folder to select file
            sg.Button("Load C1 Image", size=(10, 1))    # Button

        ],


        [
            sg.Text("C2 Image Path:", size=(20, 1)),        # Text line
            sg.Input(size=(30, 1), enable_events=True, key="-C2FILE-"),      # Input File path
            sg.FileBrowse(file_types=file_types, size=(10, 1)),     # open folder to select file
            sg.Button("Load C2 Image", size=(10, 1), )      # Button

        ],

        [
            sg.Button("get XY location", size=(20, 1))      # Button
        ]

    ]

    #   For Channel 1: Nucleus Channel
    image_viewer_column_C1 = [
        [sg.Text("C1 Image :")],
        [sg.Text(size=(40, 1), key="-C1TOUT-")],
        [sg.Image(key="-C1IMAGE-", size=(300, 300))],  # Image for Channel 1
        [sg.HSeperator()],  # Horizontal line to separate UI elements
        [sg.Image(key='-C1INTPLOT-', size=(300, 300))]  # Intensity map image for channel 1
    ]

    #   For Channel 2: Cytoplasm Channel, identical with C1
    image_viewer_column_C2 = [
        [sg.Text("C2 Image:")],
        [sg.Text(size=(40, 1), key="-C2TOUT-")],
        [sg.Image(key="-C2IMAGE-", size=(300, 300))],
        [sg.HSeperator()],
        [sg.Image(key='-C2INTPLOT-', size=(300, 300))]
    ]

    # Design Cell Annotation Column
    cell_type_classifier = [
        #   Cell index UI element
        [sg.Text('Select cell index', size=(10, 1)),
         sg.InputText(enable_events=True, key='-CELLIDX-'), sg.Button('Go')],

        # Buttons for Next image, output results, and all different cell types
        [sg.Button("Next", size=(25, 1), key='ShowNextImage')],
        [sg.Button("Result", size=(25, 1), key='-Result-')],
        [sg.Button('None', size=(25, 1))],
        [sg.Button('Normal Cell', size=(25, 1))],
        [sg.Button('CC', size=(25, 1))],
        [sg.Button('KHC', size=(25, 1))],
        [sg.Button('Folded', size=(25, 1))],
        [sg.Button('Unfocused', size=(25, 1))],
    ]

    # GUI Layout

    layout = [

            [sg.Column(file_list_column)],
            [sg.HSeperator()],
            [sg.Column(image_viewer_column_C1),
             sg.VSeperator(),
             sg.Column(image_viewer_column_C2),
             sg.VSeperator(),
             sg.Column(cell_type_classifier)],

    ]

    # Generate master Window
    window = sg.Window(title='Cell Annotation GUI', layout=layout)

    # Start Loop for GUI
    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:  # Terminate the program when hit exit
            break

        if event == 'Load C1 Image':   # When the load button is hit
            c1filename = values["-C1FILE-"]  # grab filename from key

            if os.path.exists(c1filename):
                c1image = Image.open(c1filename)  # read the input image file
                # show small size image
                imszc1 = c1image.size
                image_smc1 = c1image.resize((int(imszc1[0]/40), int(imszc1[1]/40)))

                # flush, and save the image to memory
                bio = io.BytesIO()
                image_smc1.save(bio, format="TIFF")
                window["-C1IMAGE-"].update(data=bio.getvalue())  # update C1 image window with the input image

                # convert image to gray scale
                imgint = cv2.imread(c1filename)
                img_g = imgint[:, :, 1]

                # generate intensity plot
                plt.hist(img_g.flatten(), 100, [0, 100], color='r')
                plt.savefig('C1INTMAP.PNG')  # save the plot

                # resize plot to fit window
                C1INTMAP = Image.open('C1INTMAP.PNG')
                imgszc1 = C1INTMAP.size
                C1INTMAP = C1INTMAP.resize((int(imgszc1[0]/2), int(imgszc1[1]/2)))

                # flush memory and save image to memory
                bio = io.BytesIO()
                C1INTMAP.save(bio, format="png")

                # update image to channel 1 intensity map window
                window["-C1INTPLOT-"].update(data=bio.getvalue())

        # same fot Channel 2
        if event == 'Load C2 Image':  # When a file is chosen
            c2filename = values["-C2FILE-"]
            c2image = Image.open(c2filename)

            imszc2 = c2image.size
            image_smc2 = c2image.resize((int(imszc2[0] / 40), int(imszc2[1] / 40)))

            bio = io.BytesIO()
            image_smc2.save(bio, format="TIFF")

            window["-C2IMAGE-"].update(data=bio.getvalue())

            img2int = cv2.imread(c2filename)
            img_g2 = img2int[:, :, 1]

            plt.hist(img_g2.flatten(), 100, [0, 100], color='g')
            plt.savefig('C2INTMAP.PNG')

            C2INTMAP = Image.open('C2INTMAP.PNG')
            imgszc2 = C2INTMAP.size
            C2INTMAP = C2INTMAP.resize((int(imgszc2[0] / 2), int(imgszc2[1] / 2)))

            bio = io.BytesIO()
            C2INTMAP.save(bio, format="png")

            window["-C2INTPLOT-"].update(data=bio.getvalue())

        # Get location data using nucleus detection algorism after C1 and C2 images are loaded
        if event == 'get XY location':
            try:
                # call function to generate image and location data for both channels
                c1img, Location = img_process(c1filename)
                c2img, location = img_process(c2filename)
                celltypes = [0] * len(Location)  # create list of umpty annotation data
                sg.Popup('XY location complete')    # popup notification of completion
            except:
                sg.popup_error("you need to load C1 and C2 Image first")  # popup error message when not enough input

        #  when Go botton is hit
        if event == 'Go':
            #  get cell index number
            Cellidx = int(values['-CELLIDX-'])

            if 0 < Cellidx < len(Location):  # check if index is valid
                Cur_loc = Location[Cellidx]     # get location coordinates base on index

                try:
                    show_cropped_image(c1img, Cur_loc[0], Cur_loc[1], 70)  # Generate individual cell images from original image
                    print('Cellidx1:', Cellidx)
                    print('Cur_loc:', Cur_loc)

                    c1Crop_img = Image.open('new_img.tif')  # Load the cropped image
                    c1Crop_img = c1Crop_img.resize((300, 300))  # resize image to fit window

                    # flush memory and store image in memory
                    bio = io.BytesIO()
                    c1Crop_img.save(bio, format="TIFF")

                    # update image Channel 1 image window with new cropped image
                    window["-C1IMAGE-"].update(data=bio.getvalue())

                    c1imgtif = cv2.imread('new_img.tif')  # reload the
                    c1img_g = c1imgtif[:, :, 1]  # set to gray scale
                    plt.hist(c1img_g.flatten(), 100, [0, 100], color='r')  # generate intensity plot
                    plt.savefig('C1INTMAP.PNG')

                    # resize image
                    C1INTMAP = Image.open('C1INTMAP.PNG')
                    imgszc1 = C1INTMAP.size
                    C1intmap = C1INTMAP.resize((int(imgszc1[0] / 2), int(imgszc1[1] / 2)))

                    # flush memory and store in memory
                    bio = io.BytesIO()
                    C1intmap.save(bio, format="png")

                    # update window
                    window["-C1INTPLOT-"].update(data=bio.getvalue())


                    # same for channel 2
                    show_cropped_image(c2img, Cur_loc[0], Cur_loc[1], 70)
                    c2Crop_img = Image.open('new_img.jpg')
                    c2Crop_img = c2Crop_img.resize((300, 300))
                    bio = io.BytesIO()
                    c2Crop_img.save(bio, format="TIFF")
                    window["-C2IMAGE-"].update(data=bio.getvalue())

                    c2imgjpg = cv2.imread('new_img.jpg')
                    c2img_g = c2imgjpg[:, :, 1]
                    plt.hist(c2img_g.flatten(), 100, [0, 100], color='green')
                    plt.savefig('C2INTMAP.PNG')
                    C2INTMAP = Image.open('C2INTMAP.PNG')
                    imgszc2 = C2INTMAP.size
                    C2intmap = C2INTMAP.resize((int(imgszc2[0] / 2), int(imgszc2[1] / 2)))
                    bio = io.BytesIO()
                    C2intmap.save(bio, format="png")
                    window["-C2INTPLOT-"].update(data=bio.getvalue())

                except:
                    sg.Popup('Enter index first!')
            else:
                sg.popup_error('Invalid Cell Index!')  # popup error massage when index is invalid

        # Show Next image button hit
        if event == 'ShowNextImage':

            # register cell index
            Cellidx = int(values['-CELLIDX-'])
            if 0 < Cellidx < len(Location) - 1:
                print(values['-CELLIDX-'])
                Cellidx = int(values['-CELLIDX-']) + int(1)  # go to next index
                Cur_loc = location[Cellidx]

                try:
                    show_cropped_image(c1img, Cur_loc[0], Cur_loc[1], 70)
                    print(Cur_loc)
                    c1Crop_img = Image.open('new_img.tif')
                    c1Crop_img = c1Crop_img.resize((300, 300))
                    bio = io.BytesIO()
                    c1Crop_img.save(bio, format="TIFF")
                    window["-C1IMAGE-"].update(data=bio.getvalue())

                    c1imgjpg = cv2.imread('new_img.tif')
                    c1img_g = c1imgjpg[:, :, 1]
                    plt.hist(c1img_g.flatten(), 100, [0, 100], color='r')
                    plt.savefig('C1INTMAP.PNG')
                    C1INTMAP = Image.open('C1INTMAP.PNG')
                    imgszc1 = C1INTMAP.size
                    C1intmap = C1INTMAP.resize((int(imgszc1[0] / 2), int(imgszc1[1] / 2)))
                    bio = io.BytesIO()
                    C1intmap.save(bio, format="png")
                    window["-C1INTPLOT-"].update(data=bio.getvalue())

                    show_cropped_image(c2img, Cur_loc[0], Cur_loc[1], 70)
                    c2Crop_img = Image.open('new_img.tif')
                    c2Crop_img = c2Crop_img.resize((300, 300))
                    bio = io.BytesIO()
                    c2Crop_img.save(bio, format="TIFF")
                    window["-C2IMAGE-"].update(data=bio.getvalue())

                    c2imgjpg = cv2.imread('new_img.tif')
                    c2img_g = c2imgjpg[:, :, 1]
                    plt.hist(c2img_g.flatten(), 100, [0, 100], color='g')
                    plt.savefig('C2INTMAP.PNG')
                    C2INTMAP = Image.open('C2INTMAP.PNG')
                    imgszc2 = C2INTMAP.size
                    C2INTMAP = C2INTMAP.resize((int(imgszc2[0] / 2), int(imgszc2[1] / 2)))
                    bio = io.BytesIO()
                    C2INTMAP.save(bio, format="png")
                    window["-C2INTPLOT-"].update(data=bio.getvalue())

                    window['-CELLIDX-'].update(Cellidx)

                except Cellidx == None or Cellidx > len(Location):
                    sg.popup_error('Invalid Cell Index!')
            else:
                sg.popup_error('Invalid Cell Index!')

        # assign cell type number to cell type list
        if event == 'None':
            celltypes[Cellidx] = 0
            print(celltypes[Cellidx])
            print(Cellidx)
        if event == 'Normal Cell':
            celltypes[Cellidx] = 1
            print(celltypes[Cellidx])
            print(Cellidx)
        if event == 'CC':
            celltypes[Cellidx] = 2
            print(celltypes[Cellidx])
            print(Cellidx)
        if event == 'KHC':
            celltypes[Cellidx] = 3
            print(celltypes[Cellidx])
            print(Cellidx)
        if event == 'Folded':
            celltypes[Cellidx] = 4
            print(celltypes[Cellidx])
            print(Cellidx)
        if event == 'Unfocused':
            celltypes[Cellidx] = 5
            print(celltypes[Cellidx])
            print(Cellidx)

        if event == '-Result-':
            # turn data in to dataframe
            df_loc = pd.DataFrame(Location)
            df_result = pd.DataFrame(celltypes)
            result = pd.concat([df_result, df_loc], axis=1)

            # save to .csv file
            result.to_csv('Annotation_Result.csv')
            sg.Popup('Results Saved!', keep_on_top=True)


if __name__ == '__main__':
    main()
