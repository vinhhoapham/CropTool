from PIL import Image
from Resolution import Resolution
from Coordinate import Coordinate
import numpy as np
from Settings import Settings
import PathHandling
from ImageHandling import add_circle_to_grayscale_image


def calculate_average_pixel_value(image_array):
    mask = image_array != -1
    values = image_array[mask]
    return int(np.mean(values))


class ImageModel:
    def __init__(self):
        self.image = None
        self.zoom_factor = 1.0
        self.path = None
        self.new_image_resolution = Resolution(1920, 1080)
        self.image_displacement = Coordinate(0, 0)
        self.settings = Settings()
        self.new_image_resolution = self.settings.output_image_resolution

    def load_image(self, file_path):
        self.image = Image.open(file_path).convert('L')

    def zoom_in(self):
        self.zoom_factor *= 1.1

    def zoom_out(self):
        self.zoom_factor /= 1.1

    def get_resized_image(self):
        if self.image:
            return self.image.resize(
                (int(self.image.size[0] * self.zoom_factor),
                 int(self.image.size[1] * self.zoom_factor)),
                Image.Resampling.LANCZOS)
        return None

    def crop_image_array(self, crop_coords):
        current_image = self.get_resized_image()
        current_image_array = np.array(current_image)
        zero_pixel = current_image_array == 0
        current_image_array[zero_pixel] = 1
        current_image = Image.fromarray(current_image_array, 'L')
        cropped_image = current_image.crop(crop_coords)
        cropped_image_array = np.array(cropped_image).astype(np.int16)
        black_pixel = cropped_image_array == 0
        cropped_image_array[black_pixel] = -1
        return cropped_image_array

    def fill_image(self, crop_coords):
        # Plus the displacement to the crop coordinates
        crop_coords = (crop_coords[0] + self.image_displacement.row,
                       crop_coords[1] + self.image_displacement.col,
                       crop_coords[2] + self.image_displacement.row,
                       crop_coords[3] + self.image_displacement.col)

        cropped_image_array = self.crop_image_array(crop_coords)

        avg_pixel_value = calculate_average_pixel_value(cropped_image_array)
        mask = cropped_image_array == -1

        filled_image_array = cropped_image_array
        filled_image_array[mask] = avg_pixel_value
        filled_image_array = filled_image_array.astype(np.uint8)
        filled_image = Image.fromarray(filled_image_array, 'L')
        return filled_image

    def export_image(self, image, file_path=None):
        if file_path is None:
            # Use settings to determine the save location and filename
            _, _, file_name, ext = PathHandling.get_default_cropped_file_path(self.path)
            save_directory = self.settings.default_save_path

            if self.settings.save_pic_with_no_circle:
                save_path = PathHandling.generate_save_path(save_directory, file_name, ext, "cropped")
                image.save(save_path)
            if self.settings.save_pic_with_circle:
                diameter = self.settings.circle_diameter
                image_with_circle = add_circle_to_grayscale_image(image.copy(), diameter)
                save_path = PathHandling.generate_save_path(save_directory, file_name, ext, "cropped_with_circle")
                image_with_circle.save(save_path)
        else:
            image.save(file_path)
