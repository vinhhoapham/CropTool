class ImageViewModel:
    def __init__(self, model):
        self.model = model

    def load_image(self, file_path):
        self.model.load_image(file_path)

    def zoom_in(self):
        self.model.zoom_in()

    def zoom_out(self):
        self.model.zoom_out()

    def get_resized_image(self):
        return self.model.get_resized_image()

    def fill_image(self, crop_coords):
        return self.model.fill_image(crop_coords)

    def get_image(self):
        return self.model.image

    def is_image_loaded(self):
        return self.model.image is not None

    def get_zoom_level(self):
        return self.model.zoom_factor

    def update_image_path(self, image_path):
        self.model.path = image_path

    def export_image(self, image, file_path):
        self.model.export_image(image, file_path)

    def move_image(self, vector):
        self.model.image_displacement.move(vector)

    def get_file_path(self):
        return self.model.path

