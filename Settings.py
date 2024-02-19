import os
from Resolution import Resolution


class Settings:

    def __init__(self):
        self.default_save_path = ""
        self.save_pic_with_circle = True
        self.save_pic_with_no_circle = True
        self.output_image_resolution = Resolution(1920, 1080)
        self.ask_for_directory_when_saving = False
        self.circle_diameter = 236

        if os.path.exists("settings.txt"):
            self.import_from_file()
        else:
            self.default_save_path = os.getcwd()
            self.export_to_file()

    def export_to_file(self):
        with open("settings.txt", "w") as file:
            file.write(f"default_save_path={self.default_save_path}\n")
            file.write(f"save_pic_with_circle={self.save_pic_with_circle}\n")
            file.write(f"save_pic_with_no_circle={self.save_pic_with_no_circle}\n")
            file.write(f"output_image_resolution={self.output_image_resolution}\n")
            file.write(f"ask_for_directory_when_saving={self.ask_for_directory_when_saving}\n")
            file.write(f"circle_diameter={self.circle_diameter}\n")

    def import_from_file(self):
        with open("settings.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                if key == "default_save_path":
                    self.default_save_path = value
                elif key == "save_pic_with_circle":
                    self.save_pic_with_circle = value.lower() == 'true'
                elif key == "save_pic_with_no_circle":
                    self.save_pic_with_no_circle = value.lower() == 'true'
                elif key == "output_image_resolution":
                    width, height = map(int, value.split('x'))
                    self.output_image_resolution = Resolution(width, height)
                elif key == "ask_for_directory_when_saving":
                    self.ask_for_directory_when_saving = value.lower() == 'true'
                elif key == "circle_diameter":
                    self.circle_diameter = int(value)

    def update_default_save_path(self, new_path):
        self.default_save_path = new_path
        self.export_to_file()

    def update_resolution(self, width, height):
        self.output_image_resolution = Resolution(width, height)
        self.export_to_file()

    def update_option(self, option_name, option_value):
        if option_name == "save_pic_with_circle":
            self.save_pic_with_circle = option_value
        elif option_name == "save_pic_with_no_circle":
            self.save_pic_with_no_circle = option_value
        elif option_name == "output_image_resolution":
            width, height = map(int, option_value.split('x'))
            self.output_image_resolution = Resolution(width, height)
        elif option_name == "circle_diameter":
            self.circle_diameter = int(option_value)
        self.export_to_file()

    def update_ask_for_directory(self, value):
        self.ask_for_directory_when_saving = value
        self.export_to_file()

    def update_circle_diameter(self, new_diameter):
        self.circle_diameter = new_diameter
        self.export_to_file()
