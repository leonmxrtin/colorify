import spotipy

class SpotifyClient():
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self._oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
        self._spotify = spotipy.Spotify(auth_manager=self._oauth)

    def get_currently_playing(self):
        current_track = self._spotify.current_user_playing_track()

        if current_track and current_track['item']['album']['images']:
            images = current_track['item']['album']['images']

            is_playing = current_track['is_playing']
            artwork_url = images[0]['url']
            timestamp = current_track['timestamp']
        else:
            is_playing = False
            artwork_url = None
            timestamp = 0

        return is_playing, artwork_url, timestamp