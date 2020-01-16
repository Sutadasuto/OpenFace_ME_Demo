import os
import shutil
import argparse
import csv
import datetime
from tkinter import *
from graphs import gui


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("openface_path", type=str)
    parser.add_argument("--output_folder", type=str, default=os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    parser.add_argument("--device_id", type=int, default=0)
    return parser.parse_args(args)
    

def main(args):
    command = '%s -device %s -vis-aus -pose -aus -gaze -simalign -tracked -g -out_dir "%s"' % (os.path.join(args.openface_path, "build", "bin", "FeatureExtraction").replace(" ", "\ "), args.device_id, args.output_folder)
    os.system(command)
 
    app = gui(outputFolder)
    app.mainloop()


if __name__ == "__main__":
    args = parse_args()
    main(args)
