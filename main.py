from rgb import MatrixController
from spotify import SpotifyClient

import requests
from PIL import Image

from time import time_ns, sleep
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

client = SpotifyClient(config['Spotify']['ClientID'], config['Spotify']['ClientSecret'], 
                       config['Spotify']['RedirectURI'], config['Spotify']['Scope'])

matrix_controller = MatrixController(int(config['Matrix']['Size']), config['Matrix']['Mapping'])

paused = False
prev_artwork_url = ""

while True:
    is_playing, artwork_url, timestamp = client.get_currently_playing()

    if is_playing and artwork_url != prev_artwork_url: # playing new track
        paused = False
        prev_artwork_url = artwork_url
        artwork = client.fetch_artwork(artwork_url)

        matrix_controller.transition(artwork)
    elif is_playing and paused: # resumed playing
        paused = False
        matrix_controller.brighten()
    elif not is_playing and time_ns()//1000000 < timestamp + int(config['General']['PauseTimeout']) * 1000:
        paused = True
        matrix_controller.dim(int(config['General']['PauseBrightness']))
    elif not is_playing: # no track playing
        paused = False
        prev_artwork_url = ""
        matrix_controller.dim()
    
    sleep(5)