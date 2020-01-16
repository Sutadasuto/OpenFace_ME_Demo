import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import csv
import tkinter as tk
from tkinter import ttk
import os


LARGE_FONT= ("Verdana", 12)


class gui(tk.Tk):

    def __init__(self, processedFolder, *args, **kwargs):

        csv_files = sorted([f for f in os.listdir(processedFolder) if
                               os.path.isfile(os.path.join(processedFolder, f))
                               and not f.startswith('.') and f[-4:].lower() == ".csv"],
                              key=lambda f: f.lower())

        if len(csv_files) == 1:
            with open(os.path.join(processedFolder, csv_files[0])) as csv_file:
                reader = csv.reader(csv_file)
                self.openface_matrix = []
                for row in reader:
                    self.openface_matrix.append(row)
            self.available_aus = []
            for cell in self.openface_matrix[0]:
                if "_r" in cell:
                    self.available_aus.append(cell.split("_r")[0][1:])
        else:
            print("Be sure that 1 and only 1 .csv is available in the folder.")
            raise FileExistsError

        folders = sorted([f for f in os.listdir(processedFolder) if
                               os.path.isdir(os.path.join(processedFolder, f))
                               and not f.startswith('.')],
                              key=lambda f: f.lower())

        if len(folders) == 1:
            pics_folder = os.path.join(processedFolder, folders[0])
            self.image_files = sorted([os.path.join(pics_folder, f)
                                       for f in os.listdir(pics_folder) if
                                       os.path.isfile(os.path.join(pics_folder, f)) and
                                       not f.startswith('.')], key=lambda  f: f.lower())
        else:
            print("Be sure that 1 and only 1 folder is available in the folder.")
            raise FileExistsError

        self.current_frame = 1

        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Analysis")
        tk.Tk.wm_attributes(self, "-fullscreen", True)
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Page):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, name):
        self.frames[name].tkraise()

    def exit_gui(self):
        self.quit()
        self.destroy()

    def change_plot(self, au):
        if au in [item.lstrip("AU").lstrip("0") for item in self.available_aus] and len(au)>0:
            frame = self.frames[Page]
            au_index = self.openface_matrix[0].index(" AU%s_r" % au.zfill(2))
            ts_index = self.openface_matrix[0].index(" timestamp")
            x = []
            y = []
            for row in self.openface_matrix[1:]:
                x.append(float(row[ts_index]))
                y.append(float(row[au_index]))
            frame.independent_values = x
            frame.dependent_values = y
            frame.draw_plot(x,y,au)
            frame.tkraise()
        else:
            frame = self.frames[StartPage]
            frame.text_box.insert(10,": Invalid AU")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.matrix = controller.openface_matrix
        label = tk.Label(self, text="WELCOME!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label2 = tk.Label(self, text="Write down the AU of interest and click the button to analyze.", font=LARGE_FONT)
        label2.pack()

        self.text_box = tk.Entry(self)
        self.text_box.pack()
        button = ttk.Button(self, text="Analyze",
                            command=lambda: controller.change_plot(self.text_box.get()))
        button.pack()
        button2 = ttk.Button(self, text="Exit",
                            command=lambda: controller.exit_gui())
        button2.pack()
        options = "\n"
        with open("code.csv") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                options += (": ".join(row) + "\n")
        label3 = tk.Label(self, text=options, font=LARGE_FONT)
        label3.pack()


class Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.openface_matrix = controller.openface_matrix
        self.f_index = self.openface_matrix[0].index("frame")
        self.ts_index = self.openface_matrix[0].index(" timestamp")
        self.images = []
        for image_file in controller.image_files:
            self.images.append(mpimg.imread(image_file))
        self.current_frame = controller.current_frame
        self.title_label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        self.title_label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        self.figure = plt.figure(0)
        self.independent_values = []
        self.dependent_values = []
        self.ax = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=2)
        self.ax.set_xlabel("Time Stamp")
        self.ax.set_ylabel("Intensity")
        self.ax.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        for tick in self.ax.get_xticklabels():
            tick.set_rotation(90)

        self.picture = plt.subplot2grid((2, 3), (0, 2), colspan=1, rowspan=1)
        canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas = canvas
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(canvas, self)
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        button_next = ttk.Button(self, text="Next",
                                 command=lambda: self.draw_pic(1))
        button_next.pack(side=tk.RIGHT)
        self.current_frame_label = tk.Label(self, text=self.current_frame)
        self.current_frame_label.pack(side=tk.RIGHT)
        button_prev = ttk.Button(self, text="Prev",
                                 command=lambda: self.draw_pic(-1))
        button_prev.pack(side=tk.RIGHT)
        self.draw_pic(0)

    def draw_plot(self, x, y, au):
        self.title_label.config(text=au)
        self.ax.clear()
        self.ax.set_xlabel("Time Stamp")
        self.ax.set_ylabel("Intensity")
        self.ax.plot(x,y)
        self.ax.plot(x,[1]*len(x))
        for tick in self.ax.get_xticklabels():
            tick.set_rotation(90)
        self.canvas.draw()

        self.toolbar.destroy()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def draw_pic(self, step):

        self.current_frame += step
        if self.current_frame < 1:
            self.current_frame = len(self.images)
        elif self.current_frame > len(self.images):
            self.current_frame = 1

        if len(self.ax.lines) == 3:
            self.ax.lines[2].remove()
        current_x = float(self.ax.lines[0].get_xdata()[self.current_frame-1])
        self.ax.axvline(x=current_x)

        label = self.openface_matrix[self.current_frame][self.f_index] + ":" + \
                self.openface_matrix[self.current_frame][self.ts_index] + " s"
        img = self.images[self.current_frame - 1]

        self.current_frame_label.config(text=label)
        self.picture.imshow(img)
        self.canvas.draw()

