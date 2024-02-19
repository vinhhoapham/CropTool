from tkinter import Label, Entry, Button, Checkbutton, IntVar, Toplevel, messagebox, filedialog
from tkinter.ttk import Frame


class SettingsPopupComponent(Toplevel):
    def __init__(self, parent, image_view_model):
        super().__init__(parent)
        self.image_view_model = image_view_model

        self.title("Settings")
        self.geometry("800x600")
        self.grab_set()
        self.focus_force()

        main_frame = Frame(self)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Default save path
        folder_frame = Frame(main_frame)
        folder_frame.pack(fill='x', pady=5)
        self.folder_button = Button(folder_frame, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(side='left', padx=5)
        self.label_path = Label(folder_frame, text="Default Save Path")
        self.label_path.pack(side='left', padx=5)
        self.entry_path = Entry(folder_frame)
        self.entry_path.pack(side='left', fill='x', expand=True)
        self.entry_path.insert(0, self.image_view_model.model.settings.default_save_path)

        # Save picture options
        save_picture_frame = Frame(main_frame)
        save_picture_frame.pack(fill='x', pady=5)
        self.save_circle_var = IntVar(value=self.image_view_model.model.settings.save_pic_with_circle)
        self.check_save_circle = Checkbutton(save_picture_frame, text="Save Picture With Circle", variable=self.save_circle_var)
        self.check_save_circle.pack(side='left', padx=5)
        self.save_no_circle_var = IntVar(value=self.image_view_model.model.settings.save_pic_with_no_circle)
        self.check_save_no_circle = Checkbutton(save_picture_frame, text="Save Picture Without Circle", variable=self.save_no_circle_var)
        self.check_save_no_circle.pack(side='left', padx=5)

        # Resolution and Circle Diameter
        resolution_frame = Frame(main_frame)
        resolution_frame.pack(fill='x', pady=5)
        self.label_resolution = Label(resolution_frame, text="Output Image Resolution (Width x Height)")
        self.label_resolution.pack(side='left', padx=5)
        self.entry_resolution = Entry(resolution_frame)
        self.entry_resolution.pack(side='left', padx=5)
        resolution = self.image_view_model.model.settings.output_image_resolution
        self.entry_resolution.insert(0, f"{resolution.width}x{resolution.height}")
        self.label_diameter = Label(resolution_frame, text="Circle Diameter")
        self.label_diameter.pack(side='left', padx=5)
        self.entry_diameter = Entry(resolution_frame)
        self.entry_diameter.pack(side='left', padx=5)
        self.entry_diameter.insert(0, self.image_view_model.model.settings.circle_diameter)

        # Ask for directory when saving
        ask_directory_frame = Frame(main_frame)
        ask_directory_frame.pack(fill='x', pady=5)
        self.ask_directory_var = IntVar(value=self.image_view_model.model.settings.ask_for_directory_when_saving)
        self.check_ask_directory = Checkbutton(ask_directory_frame, text="Ask For Directory When Saving", variable=self.ask_directory_var)
        self.check_ask_directory.pack(side='left', padx=5)

        # Save and Close Buttons
        button_frame = Frame(main_frame)
        button_frame.pack(fill='x', pady=5)
        self.save_button = Button(button_frame, text="Save", command=self.save_settings)
        self.save_button.pack(side='left', padx=5)
        self.close_button = Button(button_frame, text="Close", command=self.destroy)
        self.close_button.pack(side='left', padx=5)

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

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_path.delete(0, 'end')
            self.entry_path.insert(0, folder_selected)