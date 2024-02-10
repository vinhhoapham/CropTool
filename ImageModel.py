from PIL import Image
from Resolution import Resolution
from Coordinate import Coordinate
import numpy as np


class ImageModel:
    def __init__(self):
        self.image = None
        self.zoom_factor = 1.0
        self.path = None
        self.new_image_resolution = Resolution(1920, 1080)
        self.image_displacement = Coordinate(0, 0)

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

        avg_pixel_value = self.calculate_average_pixel_value(cropped_image_array)
        mask = cropped_image_array == -1

        filled_image_array = cropped_image_array
        filled_image_array[mask] = avg_pixel_value
        filled_image_array = filled_image_array.astype(np.uint8)
        filled_image = Image.fromarray(filled_image_array, 'L')
        return filled_image

    def calculate_average_pixel_value(self, image_array):
        mask = image_array != -1
        values = image_array[mask]
        return int(np.mean(values))

    def export_image(self, image, file_path):
        image.save(file_path)



