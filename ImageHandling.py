from PIL import Image, ImageDraw


def add_circle_to_grayscale_image(image, diameter):
    # Check if the image is already grayscale
    if image.mode != 'L':
        raise ValueError("The image must be in grayscale mode ('L').")

    draw = ImageDraw.Draw(image)
    width, height = image.size
    left = (width - diameter) / 2
    top = (height - diameter) / 2
    right = (width + diameter) / 2
    bottom = (height + diameter) / 2

    # Draw a white circle (0 in grayscale) on the grayscale image
    draw.ellipse([left, top, right, bottom], outline=255, width=10)

    return image
