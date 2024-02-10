from tkinter import Canvas


class CanvasComponent:
    def __init__(self, master, on_move_press, on_click):
        self.canvas = Canvas(master, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Motion>", on_move_press)
        self.canvas.bind("<Button-1>", on_click)
        self.image_on_canvas = None

    def add_image(self, tk_image):
        if self.image_on_canvas:
            self.canvas.itemconfig(self.image_on_canvas, image=tk_image)
        else:
            self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=tk_image)

    def move_image(self, dx, dy):
        self.canvas.move(self.image_on_canvas, dx, dy)

    def update_image(self, tk_image):
        self.canvas.itemconfig(self.image_on_canvas, image=tk_image)
