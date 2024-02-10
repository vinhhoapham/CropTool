import os


def get_default_cropped_file_path(original_file_path):
    original_dir, original_file = os.path.split(original_file_path)
    file_name, file_extension = os.path.splitext(original_file)
    default_cropped_file_path = os.path.join(original_dir, f"{file_name}_cropped{file_extension}")
    return default_cropped_file_path, original_dir, file_name, file_extension


def get_dir(file_path):
    return os.path.dirname(file_path)
