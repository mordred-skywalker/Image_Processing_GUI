import PySimpleGUIQt as sg
import cv2
import numpy as np

def main():
    sg.theme('LightGreen')

    layout = [
        [sg.Text('opencv', size=(60,1),
                 justification='center')],
        [sg.Image(filename='', key='-IMAGE-')],

        [
            sg.Radio('None', 'Radio', True, size=(10,1))
        ],

        [
            sg.Radio('threshold', 'radio', size=(10,1), key='-THRESH-'),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation='h',
                size=(40,15),
                key='-THRESH SLIDER-',
            ),
        ],


        [sg.Button('Exit', size=(10,1))]
    ]

    window = sg.Window('openCv', layout, location=(800,400))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event ==sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)

    window.close()

if __name__ == '__main__':
    main()