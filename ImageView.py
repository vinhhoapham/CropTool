from tkinter import Tk, filedialog
from PIL import ImageTk, Image

from MenuBarComponent import MenuBarComponent
from StatusBarComponent import StatusBarComponent
from CanvasComponent import CanvasComponent
from ControlPanelComponent import ControlPanelComponent
from PathHandling import get_default_cropped_file_path, get_dir


class ImageView:
    def __init__(self, master, view_model, rectangle_size=(1920, 1080)):
        self.master = master
        self.view_model = view_model
        self.master.attributes('-fullscreen', True)
        self.rectangle_size = rectangle_size
        self.zoom_constant = 20
        self.crop_rectangle = None
        self.center_circle = None
        self.tk_image = None
        self.image_on_canvas = None
        self.master.title = 'Crop and Center Tool'

        # Initialize components
        self.menubar = MenuBarComponent(master, self.load_image, master.quit)
        self.status_bar = StatusBarComponent(master)
        self.control_panel = ControlPanelComponent(master, self.load_image, self.zoom_in, self.zoom_out)
        self.canvas_component = CanvasComponent(master, self.on_move_press, self.crop_image)

        # Bind keyboard events for image movement
        self.canvas_component.canvas.focus_set()
        self.canvas_component.canvas.bind("<Left>", self.move_left)
        self.canvas_component.canvas.bind("<Right>", self.move_right)
        self.canvas_component.canvas.bind("<Up>", self.move_up)
        self.canvas_component.canvas.bind("<Down>", self.move_down)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.view_model.load_image(file_path)
            self.view_model.update_image_path(file_path)
            self.tk_image = ImageTk.PhotoImage(self.view_model.get_image())
            if self.image_on_canvas:
                self.canvas_component.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)
            else:
                self.image_on_canvas = self.canvas_component.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def zoom_in(self):
        self.view_model.zoom_in()
        self.update_image()

    def zoom_out(self):
        self.view_model.zoom_out()
        self.update_image()

    def update_image(self):
        resized_image = self.view_model.get_resized_image()
        if resized_image:
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas_component.canvas.itemconfig(self.image_on_canvas, image=self.tk_image)

    def on_move_press(self, event):
        if not self.view_model.is_image_loaded():
            return

        curX, curY = self.canvas_component.canvas.canvasx(event.x), self.canvas_component.canvas.canvasy(event.y)
        startX, startY = curX - self.rectangle_size[0] / 2, curY - self.rectangle_size[1] / 2
        endX, endY = curX + self.rectangle_size[0] / 2, curY + self.rectangle_size[1] / 2

        if self.crop_rectangle:
            self.canvas_component.canvas.coords(self.crop_rectangle, startX, startY, endX, endY)
        else:
            self.crop_rectangle = self.canvas_component.canvas.create_rectangle(startX, startY, endX, endY,
                                                                                outline="red")

        self.update_center_circle(startX, startY, endX, endY)

    def update_center_circle(self, startX, startY, endX, endY):
        circle_radius = 236 / 2
        circle_centerX, circle_centerY = (startX + endX) / 2, (startY + endY) / 2

        circle_startX, circle_startY = circle_centerX - circle_radius, circle_centerY - circle_radius
        circle_endX, circle_endY = circle_centerX + circle_radius, circle_centerY + circle_radius

        if self.center_circle:
            self.canvas_component.canvas.coords(self.center_circle, circle_startX, circle_startY, circle_endX,
                                                circle_endY)
        else:
            self.center_circle = self.canvas_component.canvas.create_oval(circle_startX, circle_startY, circle_endX,
                                                                          circle_endY, outline="blue")

    def crop_image(self, event):
        if self.crop_rectangle and self.view_model.is_image_loaded():
            coords = self.canvas_component.canvas.coords(self.crop_rectangle)
            processed_image = self.view_model.fill_image(coords)
            processed_image.show()

            _, original_dir, file_name, file_extension = get_default_cropped_file_path(self.view_model.get_file_path())

            # Ask user to choose the save file path
            new_file_path = filedialog.asksaveasfilename(initialdir=original_dir,
                                                         initialfile=f"{file_name}_cropped{file_extension}",
                                                         defaultextension=file_extension,
                                                         filetypes=[("All files", "*.*")])

            # If the user provides a file path, save the image
            if new_file_path:
                self.view_model.export_image(processed_image, new_file_path)

            self.canvas_component.canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None

    def move_left(self, event):
        move_vector = (self.zoom_constant, 0)
        self.view_model.move_image(move_vector)
        self.canvas_component.canvas.move(self.image_on_canvas, -self.zoom_constant, 0)

    def move_right(self, event):
        move_vector = (-self.zoom_constant, 0)
        self.view_model.move_image(move_vector)
        self.canvas_component.canvas.move(self.image_on_canvas, self.zoom_constant, 0)

    def move_up(self, event):
        move_vector = (0, self.zoom_constant)
        self.view_model.move_image(move_vector)
        self.canvas_component.canvas.move(self.image_on_canvas, 0, -self.zoom_constant)

    def move_down(self, event):
        move_vector = (0, -self.zoom_constant)
        self.view_model.move_image(move_vector)
        self.canvas_component.canvas.move(self.image_on_canvas, 0, self.zoom_constant)
