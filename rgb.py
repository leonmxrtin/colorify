import requests
from time import sleep
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class MatrixController():
    def __init__(self, size, mapping):
        self._options = RGBMatrixOptions()
        self._options.rows = self._options.cols = size
        self._options.chain_length = 1
        self._options.parallel = 1
        self._options.hardware_mapping = mapping

        self._matrix = RGBMatrix(options=self._options)
        self._current_image = Image.new('RGB', (self._matrix.width, self._matrix.height))
        self._matrix.SetImage(self._current_image)

    def fade_in(self, image, delay=0.001, max_brightness=100):
        while self._matrix.brightness <= max_brightness:
            self._matrix.brightness += 1
            self._matrix.SetImage(image)
            sleep(delay)

    def fade_out(self, image, delay=0.001, min_brightness=0):
        while self._matrix.brightness >= min_brightness:
            self._matrix.brightness -= 1
            self._matrix.SetImage(image)
            sleep(delay)

    def dim(self, brightness):
        self.fade_out(self._current_image, min_brightness=brightness)

    def set_image(self, image, brightness=100):
        if image.size != (self._matrix.width, self._matrix.height):
            image = image.resize((self._matrix.width, self._matrix.height), resample=Image.Resampling.LANCZOS).convert('RGB')

        self.fade_out(self._current_image)
        self.fade_in(image, brightness)
        self._current_image = image

    def set_image_url(self, url):
        image = Image.open(requests.get(url, stream=True).raw)
        self.set_image(image)

    def clear(self):  
        self._matrix.Clear()