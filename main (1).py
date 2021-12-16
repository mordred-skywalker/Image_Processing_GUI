import io
import PySimpleGUIQt as sg
import os.path
from PIL import Image
import cv2
import numpy as np
from time import time,sleep
from PIL import ImageFile
from os import listdir
from os.path import isfile, join
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True


#mypath='/path/to/folder'
#onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
#images = numpy.empty(len(onlyfiles), dtype=object)
#for n in range(0, len(onlyfiles)):
  #images[n] = cv2.imread( join(mypath,onlyfiles[n]) )




def croppedimages(imagestack):
    idx = 0
    yield imagestack[idx]
    idx += idx

file_types = [("TIFF(*.tif)","*.tif")]

file_list_column = [
    [

        sg.Text("C1 Image Path:"),
        sg.Input(size=(25,1),enable_events=True, key="-C1FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Load C1 Image")

    ],


    [
        sg.Text("C2 Image Path:"),
        sg.Input(size=(25, 1), enable_events=True, key="-C2FILE-"),
        sg.FileBrowse(file_types=file_types),
        sg.Button("Load C2 Image")

    ],

]

image_viewer_column_C1 = [
    [sg.Text("C1 Image :")],
    [sg.Text(size=(40,1), key="-C1TOUT-")],
    [sg.Image(key="-C1IMAGE-", size=(300,300))],
]
image_viewer_column_C2 = [
    [sg.Text("C2 Image:")],
    [sg.Text(size=(40,1), key="-C2TOUT-")],
    [sg.Image(key="-C2IMAGE-", size=(300,300))],
]

cell_type_classifier = [
    [sg.Text("WHAT TYPE IS THIS:")],
    [sg.Input(size=(25, 1), enable_events=True, key="-CELLTYPE-")],
    [sg.Radio('None', 'Radio', True, size=(25,1))],
    [sg.Radio('Type 0', 'Radio', True, size=(25,1), key='-CellTypeButton-')],
    [sg.Radio('Type 1', 'Radio', True, size=(25,1), key='-CellTypeButton-')],
]

dialog_box = [
    [sg.Text(size=(40,1), key="-output message-")],
]

Next_button = [
    [sg.Button("Next")]
]
# Layout

layout = [

        [sg.Column(file_list_column)],
        [sg.HSeperator()],
        [sg.Column(image_viewer_column_C1), sg.VSeperator(), sg.Column(image_viewer_column_C2), sg.VSeperator(), sg.Column(cell_type_classifier)],

        [sg.Column(dialog_box)],

]

# Window
window = sg.Window(title='Cell Annotation GUI', layout=layout)

while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == 'Load C1 Image': #When a file is chosen
        # foldername = values["-FOLDER-"]
        filename = values["-C1FILE-"]
        if os.path.exists(filename):
            image = Image.open(filename)
            # show small size image
            imszc1 = image.size
            #image_1 = np.array(Image.fromarray(image).resize(imsz[0]/10,imsz[1]/10))
            image_smc1 = image.resize((int(imszc1[0]/20),int(imszc1[1]/20)))
            bio = io.BytesIO()
            image_smc1.save(bio, format="TIFF")
            window["-C1IMAGE-"].update(data=bio.getvalue())
            # run cell detection on the image with multiple cells
            # xycoord = celldetection(image)
            # imagestack = cropimages(image,xycoord) #crop images at xycoord and return as imagestack as variable type "generator"

    if event == 'Load C2 Image':  # When a file is chosen
        filename = values["-C2FILE-"]
        if os.path.exists(filename):
            image = Image.open(filename)
            # show small size image
            imszc2 = image.size
            # image_1 = np.array(Image.fromarray(image).resize(imsz[0]/10,imsz[1]/10))
            image_smc2 = image.resize((int(imszc2[0] / 20), int(imszc2[1] / 20)))
            bio = io.BytesIO()
            image_smc2.save(bio, format="TIFF")
            window["-C2IMAGE-"].update(data=bio.getvalue())

    if event == 'Show Next Image':
        try:
            g = croppedimages()
            crop = g.next()
            bio = io.BytesIO()
            crop.save(bio, format="TIFF")
            window["-C1IMAGE-"].update(data=bio.getvalue())
        except:
            window["-output message-"].update(data="you need to load C1 Image first")

    celltypes =[]
    if event == 'CellTypeButton':
        celltypes.append(values["-CellTypeButton-"])







