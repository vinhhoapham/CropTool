from PIL import Image
from Resolution import Resolution
import os


class ImageModel:
    def __init__(self):
        self.image = None
        self.zoom_factor = 1.0
        self.path = None
        self.new_image_resolution = Resolution(1920, 1080)  # Default resolution

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

    def crop_image(self, crop_coords):
        real_crop_coords = [int(coord / self.zoom_factor) for coord in crop_coords]
        print(f"{real_crop_coords}, image size: {self.image.size}")
        cropped_image = self.image.crop(real_crop_coords)
        return cropped_image

    def fill_image(self, crop_coords):
        cropped_image = self.crop_image(crop_coords)
        avg_pixel_value = self.calculate_average_pixel_value(cropped_image)

        for x in range(cropped_image.width):
            for y in range(cropped_image.height):
                if not self.is_inside_picture((x, y)):
                    cropped_image.putpixel((x, y), avg_pixel_value)
        print(f"Average pixel_value: {avg_pixel_value}")

        # Resize the cropped image to new resolution
        filled_image = cropped_image.resize((self.new_image_resolution.width, self.new_image_resolution.height), Image.Resampling.LANCZOS)

        return filled_image

    def calculate_average_pixel_value(self, image):
        inside_pixels = [(x, y) for x in range(image.width)
                                  for y in range(image.height)
                                  if self.is_inside_picture((x, y))]

        if not inside_pixels:
            return 0

        total_value = sum(image.getpixel(coord) for coord in inside_pixels)
        return total_value // len(inside_pixels)

    def export_image(self, image):
        directory = os.path.dirname(self.path)
        file_name, file_ext = os.path.splitext(os.path.basename(self.path))
        new_file_name = f"{file_name}_cropped{file_ext}"
        new_file_path = os.path.join(directory, new_file_name)
        image.save(new_file_path)

    def is_inside_picture(self, coord):
        if self.image is None:
            return False

        image_width, image_height = self.image.size
        x, y = coord

        # Check if the coordinate is within the image boundaries
        return 0 <= x < image_width and 0 <= y < image_height

