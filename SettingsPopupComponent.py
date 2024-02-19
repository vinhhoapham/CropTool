from tkinter import Label, Entry, Button, Checkbutton, IntVar, Toplevel, messagebox


class SettingsPopupComponent(Toplevel):
    def __init__(self, parent, image_view_model):
        super().__init__(parent)
        self.image_view_model = image_view_model

        self.title("Settings")

        # Default save path
        self.label_path = Label(self, text="Default Save Path")
        self.entry_path = Entry(self)
        self.entry_path.insert(0, self.image_view_model.model.settings.default_save_path)
        self.label_path.pack()
        self.entry_path.pack()

        # Save picture with circle
        self.save_circle_var = IntVar(value=self.image_view_model.model.settings.save_pic_with_circle)
        self.check_save_circle = Checkbutton(self, text="Save Picture With Circle", variable=self.save_circle_var)
        self.check_save_circle.pack()

        # Save picture without circle
        self.save_no_circle_var = IntVar(value=self.image_view_model.model.settings.save_pic_with_no_circle)
        self.check_save_no_circle = Checkbutton(self, text="Save Picture Without Circle",
                                                variable=self.save_no_circle_var)
        self.check_save_no_circle.pack()

        # Resolution
        self.label_resolution = Label(self, text="Output Image Resolution (Width x Height)")
        self.entry_resolution = Entry(self)
        resolution = self.image_view_model.model.settings.output_image_resolution
        self.entry_resolution.insert(0, f"{resolution.width}x{resolution.height}")
        self.label_resolution.pack()
        self.entry_resolution.pack()

        # Ask for directory when saving
        self.ask_directory_var = IntVar(value=self.image_view_model.model.settings.ask_for_directory_when_saving)
        self.check_ask_directory = Checkbutton(self, text="Ask For Directory When Saving",
                                               variable=self.ask_directory_var)
        self.check_ask_directory.pack()

        # Save Button
        self.save_button = Button(self, text="Save", command=self.save_settings)
        self.save_button.pack()

        # Close Button
        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack()

        # Circle Diameter
        self.label_diameter = Label(self, text="Circle Diameter")
        self.entry_diameter = Entry(self)
        self.entry_diameter.insert(0, self.image_view_model.model.settings.circle_diameter)
        self.label_diameter.pack()
        self.entry_diameter.pack()

        self.geometry("800x600")
        self.grab_set()
        self.focus_force()

    def save_settings(self):
        # Update settings through the image view model
        self.image_view_model.update_default_save_path(self.entry_path.get())
        self.image_view_model.update_save_pic_with_circle(bool(self.save_circle_var.get()))
        self.image_view_model.update_save_pic_with_no_circle(bool(self.save_no_circle_var.get()))
        width, height = map(int, self.entry_resolution.get().split('x'))
        self.image_view_model.update_output_image_resolution(width, height)
        self.image_view_model.update_ask_for_directory_when_saving(bool(self.ask_directory_var.get()))
        new_diameter = int(self.entry_diameter.get())
        self.image_view_model.update_circle_diameter(new_diameter)

        messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
        self.destroy()

