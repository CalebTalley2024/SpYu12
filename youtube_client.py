
# this is what will interact with the youtube API:

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

class Playlist(object):
    def __init__( id, title):
        self.id = id
        self.title = title


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track


# copied from youtube API
class YouTubeClient(object):
    def __init__(self, credentials_location):
        youtube_dl.utils.std_headers[
            'User-Agent'] = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"


        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
           credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client




# returns all of the playlists
    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part = "id, snippet",
            maxResults = 50, # max amount of songs
            mine = True
        )

        response = request.execute() # executes the request

        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return playlists


# returns videos from certain list
    def get_videos_from_playlist(self ,playlist_id):
        songs = [] # songs is an array
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id, snippet"
        )

        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist ,track = self.get_artist_and_track_from_video \
                (video_id) # will use youtube dl library  to get the video id
            if artist and track:
                songs.append \
                    (Song(artist, track)) # here, we are creating and adding a Song item with the right artist and track

        return songs

    def get_artist_and_track_from_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}" # youtube link without that video id







        # talked about @ 9:33










        video =  youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False # this is set to false so we do not download the video
        )

        artist = video['artist']
        track = video['track']

        return artist , track
