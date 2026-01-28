from time import sleep
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class MatrixController():
    def __init__(self, options):
        self._options = RGBMatrixOptions()
        self._options.drop_privileges = False # prevents file r/w errors
        for key, value in options.items():
            setattr(self._options, key, value)

        self._matrix = RGBMatrix(options=self._options)
        self._current_image = Image.new("RGB", (self._matrix.width, self._matrix.height))

    def set_image(self, image):
        matrix_size = (self._matrix.width, self._matrix.height)

        if image.size != matrix_size:
            image.thumbnail(matrix_size, Image.Resampling.LANCZOS)

        self._matrix.SetImage(image)
        self._current_image = image

    def brighten(self, delay=0.001, max_brightness=100):
        while self._matrix.brightness < max_brightness:
            self._matrix.brightness += 1
            self._matrix.SetImage(self._current_image) # we need to refresh the image for brightness to change
            sleep(delay)

    def dim(self, delay=0.001, min_brightness=0):
        while self._matrix.brightness > min_brightness:
            self._matrix.brightness -= 1
            self._matrix.SetImage(self._current_image)
            sleep(delay)

    def transition(self, new_image, delay=0.001, max_brightness=100):
        self.dim()
        self.set_image(new_image)
        self.brighten(delay=delay, max_brightness=max_brightness)