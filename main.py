from spotify import SpotifyClient
from rgb import MatrixController
import config

from time import time_ns, sleep

spotify_client = SpotifyClient(config.spotify)
matrix_controller = MatrixController(config.matrix)

paused = False
prev_artwork_url = ""

while True:
    is_playing, artwork_url, timestamp = spotify_client.get_currently_playing()

    if is_playing and artwork_url != prev_artwork_url: # playing new track
        paused = False
        prev_artwork_url = artwork_url

        artwork = spotify_client.fetch_artwork(artwork_url)
        matrix_controller.transition(artwork)
    elif is_playing and paused: # resumed playing
        paused = False
        
        matrix_controller.brighten()
    elif not is_playing and time_ns()//1000000 < timestamp + config.pause_timeout * 1000:
        paused = True

        matrix_controller.dim(config.pause_brightness)
    elif not is_playing: # no track playing
        paused = False
        prev_artwork_url = ""

        matrix_controller.dim()
    
    sleep(5)