# OpenFace_ME_Demo
Frame analysis of Micro-Expressions detected from webcam

Tested on Ubuntu 16.04 using Python 3.5, and on Ubuntu 18.04 using Python 3.8
Requiered dependencies:

* Matplotlib
* Pillow

This work was developed using OpenFace (https://github.com/TadasBaltrusaitis/OpenFace/wiki) to extract features. Of particular interest for this demo are the intensities of the detected micro-expressions (https://github.com/TadasBaltrusaitis/OpenFace/wiki/Action-Units).
* Note that you should install OpenFace on your system as explained in their Wiki in order to run this demo.

To run, you should run in terminal like:
```
python LiveDemo.py "/path/to/OpenFace"
```

You can also change the input device (most integrated webcams are device 0) and the directory where images are saved (by default it is a folder with the current date and hour inside the root folder of the project) like this:
```
python LiveDemo.py "/home/sutadasuto/OpenFace" --device_id 0 --ouput_folder "path/to/desired/folder"
```

When you run the program, two windows will display (one showing the tracked video and another one showing the predicted ME).  When you want to stop recording, press the q key on the video stream window. You'll be taken to a new GUI, where you can analyze each ME indepently along time (frames).
