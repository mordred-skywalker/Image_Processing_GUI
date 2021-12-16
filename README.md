# Cell Annotation GUI
This is the code repository for the final Project in Software Carpentry Fall 2021. The cell annotation GUI is a graphical user interface that allows the user to select the ? as input image and annotate the image so that the user can enter a coordinate index and see the enlarged annotated cells.

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

## Setup

To set up the module, please make sure you have met all the requirements in the previous section and download the zip file for the repo to your local directory. Unzip the file into a proper folder and run the following code in commandline.

`$cd /your-filepath`

`$python3 run.py`

The cell annotation GUI will show in the Python window. For how to further navigate the cell annotation GUI, please refer to the Usage section.

## Usage

## Sources
This module is inspired by opencv [tutorial](https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/) by Adrian Rosebrock.
