# Cell Annotation GUI
This is the code repository for the final Project in Software Carpentry Fall 2021. The cell annotation GUI is a graphical user interface that allows the user to select .tiff images for individual wells in a 96 well plate as input image, and segment the image, so that the user can enter a coordinate index and see the enlarged segmented nuclues and cytoplasm. We used image segmentation to extract individual nucleus image and developed a GUI for users to easily annotate the cells according to their center coordinates. The intensity map for the segmented images will also be stored to your local directory and shown on the GUI.

![screenshot](https://github.com/mordred-skywalker/Image_Processing_GUI/blob/main/GUI_img/screenshot1.png)

## Table of contents
* [Requirements](https://github.com/mordred-skywalker/Image_Processing_GUI#Requirements)
* [Setup](https://github.com/mordred-skywalker/Image_Processing_GUI#Setup)
* [Usage](https://github.com/mordred-skywalker/Image_Processing_GUI#Usage)
* [Sources](https://github.com/mordred-skywalker/Image_Processing_GUI#Sources)

## Requirements

This module requires the following modules:

* Pillow 8.4.0 

     (See installation guide and prereqs here: https://pillow.readthedocs.io/en/stable/installation.html)
* opencv-python-headless 4.5.4.60

     (See installation guide and prereqs here: https://pypi.org/project/opencv-python-headless/)
* imutils 0.5.4
* PySimpleGUIQt 0.35.0

     (See installation guide and prereqs here: https://pypi.org/project/PySimpleGUIQt/)
* pandas
* matplotlib
* Python >= 3.8

## Setup

To set up the module, please make sure you have met all the requirements in the previous section and download the zip file for the repo to your local directory. Unzip the file into a proper folder and run the following code in commandline.

`$cd /your-filepath`

`$python3 run.py`

The cell annotation GUI will show in the Python window. For how to further navigate the cell annotation GUI, please refer to the Usage section.

## Usage

1. You can click the two browse buttons or manually input the image paths to the nuclues and cytoplasm images for the same well (please make sure you are using images from the same well or error can occur). After the correct filepaths are shown, click on 'Load C1 Image' and 'Load C2 Image'.
2. After loading the two images, the original images along with their intensity maps will be shown under 'C1 Image:' and 'C2 Image:'.
3. Clicking on 'get XY location' will return a list of coordinates for the centers of the nucleus and cytoplasm. A window pop-up will show when the procedure is completed. The preliminary results can be saved by clicking the 'Result' button on the right.
4. To show the annotated segmented image based on coordinates, enter a integer starting from 0 in the blank after 'Select cell index' and click 'Go'. The processed image will be saved locally and be shown under 'C1 Image:' and 'C2 Image:' along with new intensity maps, replacing the original images.
5. Navigate to the next coordinate by manually enter another cell index or clicking 'Next'.
6. Note that in step 4 and 5 if the input cell index is out of range (if larger than the length of the returned coordinate list), a pop-up window will occur reminding you to reenter a valid cell index.
7. To assign annotation to the segmented cell, click on the appropriate cell types shown on the right of the interface. Options include 'None' - 0, 'Normal Cell' - 1, 'CC' - 2, 'KHC' - 3, 'Folded' - 4, 'Unfocused' - 5. After annotation, the new results can be saved by clicking the 'Result' button in which the first column is the annotated value, while second/third column are the x/y coordinate for the center of the given cell.
8. After you are done with the annotation, simply close the GUI by clicking the exit button on the upperleft corner and the module will end.


## Sources
This module is inspired by opencv [tutorial](https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/) by Adrian Rosebrock.
