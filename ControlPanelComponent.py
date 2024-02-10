from tkinter import Frame, Button


class ControlPanelComponent:
    def __init__(self, master, on_load, on_zoom_in, on_zoom_out):
        self.frame = Frame(master)
        self.load_button = Button(self.frame, text="Load Image", command=on_load, bg="lightblue")
        self.zoom_in_button = Button(self.frame, text="Zoom In", command=on_zoom_in, bg="lightgreen")
        self.zoom_out_button = Button(self.frame, text="Zoom Out", command=on_zoom_out, bg="salmon")

        self.load_button.pack(side="left")
        self.zoom_in_button.pack(side="left")
        self.zoom_out_button.pack(side="left")
        self.frame.pack(pady=10)
