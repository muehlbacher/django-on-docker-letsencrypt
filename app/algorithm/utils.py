from PIL import Image


def get_image(path: str):
    image = Image.open(path)
    rgb_image = image.convert('RGB')
    return rgb_image