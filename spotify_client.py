import requests # for http requests
import urllib.parse # helps for url       ?


class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def search_song(self, artist, track):
        # query means question
        query = urllib.parse.quote(f'{artist} {track}') # urllib: url library
        # from Python API: The URL parsing functions focus on splitting a URL string into its components, or on combining URL components into a URL string.
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = request.get(
            url,

            headers={

                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"


            }


        )

        response_json = resonse.json()

        results = response_json['tracks']['items']
        if results: # if there are one or more results......

            return results[0]['id']
        else:
            raise Exception(f"No song found for {artist} = {track}")


    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response =  requests.put(
            url,
            json={
                "ids": [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }

        )

        return response.ok # checks if the request was successful