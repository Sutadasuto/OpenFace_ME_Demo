import os
import shutil
import csv
import datetime
from tkinter import *
from graphs import gui

outputFolder = "/home/sutadasuto/DemoOpenFace"

outputFolder += ("/" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

command = '/home/sutadasuto/OpenFace/build/bin/FeatureExtraction -device 0 ' \
          '-vis-aus -pose -aus -gaze -simalign -tracked -g -out_dir "' + outputFolder + '"'
os.system(command)
 

app = gui(outputFolder)
app.mainloop()