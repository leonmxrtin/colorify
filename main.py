# initialize matrix to drop privileges as soon as possible
from time import time_ns, sleep
from rgb import MatrixController
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

matrix_controller = MatrixController(int(config['Matrix']['Size']), config['Matrix']['Mapping'])

from spotify import SpotifyClient
client = SpotifyClient(config['Spotify']['ClientID'], config['Spotify']['ClientSecret'], 
                       config['Spotify']['RedirectURI'], config['Spotify']['Scope'])

matrix_controller = MatrixController(int(config['Matrix']['Size']), config['Matrix']['Mapping'])

while True:
    is_playing, artwork_url, timestamp = client.get_currently_playing()

    if not is_playing and time_ns()//1000000 > timestamp + int(config['General']['PauseTimeout']) * 1000:
        matrix_controller.clear()
    elif is_playing:
        matrix_controller.set_image_url(artwork_url)
    else:
        matrix_controller.dim(int(config['General']['PauseBrightness']))
    
    sleep(1)