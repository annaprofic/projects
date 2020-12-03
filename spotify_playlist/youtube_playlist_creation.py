import json
import requests
from projects.spotify_playlist.secrets import spotify_user_id, spotify_user_token
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


def get_youtube_client():
    """ Log Into Youtube, Copied from Youtube Data API """
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()

    # from the Youtube DATA API
    youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube_client


class CreatePlaylist:

    def __init__(self, playlist_name):
        self.playlist_name = playlist_name
        self.user_id = spotify_user_id
        self.spotify_token = spotify_user_token
        self.youtube_client = get_youtube_client()
        self.request_headers = {
                "Content_Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}"
            }

    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()
        liked_songs_info = {}
        # collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])

            # use youtube_dl to collect the song name & artist name
            video_url = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name, artist_name = video_url["track"], video_url["artist"]

            try:
                spotify_uri = self.get_spotify_song_uri(song_name, artist_name)
                liked_songs_info[video_title] = {
                    "video_url": video_url,
                    "song_name": song_name,
                    "song_artist": artist_name,

                    "spotify_uri": spotify_uri
                }
            except IndexError:
                print("[spotify] error: can't find this song", artist_name, '-', song_name)
        return liked_songs_info

    def get_playlist_info(self):
        query = 'https://api.spotify.com/v1/me/playlists'
        response = requests.get(
            query,
            headers=self.request_headers
        )

        return response.json()

    def check_for_playlist_existent(self):
        playlist = self.get_playlist_info()
        return any(tag['name'] == self.playlist_name for tag in playlist['items'])

    def get_existing_playlist_id(self):
        playlist = self.get_playlist_info()
        return [curr_playlist['id'] for curr_playlist in playlist['items']
                if curr_playlist['name'] == self.playlist_name]

    def create_playlist(self):
        request_body = json.dumps({
              "name": self.playlist_name,
              "description": "playlist contains liked songs from youtube account",
              "public": True
        })
        query = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'

        response = requests.post(
            query,
            headers=self.request_headers,
            data=request_body
        )
        return response.json()["id"]

    def get_spotify_song_uri(self, song_name, artist):
        query = f'https://api.spotify.com/v1/search?q={artist}%20-%20{song_name}&type=track&limit=20&offset=0'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        songs_list = response.json()["tracks"]["items"]
        return songs_list[0]["uri"]

    def add_song_to_spotify_playlist(self):
        liked_songs_info = self.get_liked_videos()

        songs_uris = []
        for song, info in liked_songs_info.items():
            songs_uris.append(info['spotify_uri'])

        if self.check_for_playlist_existent():
            print(f'[spotify] playlist "{self.playlist_name}" is already exist.')
            print(f'[spotify] getting playlist "{self.playlist_name}" id.')

            playlist_id = self.get_existing_playlist_id()
        else:
            print(f'[spotify] creating playlist "{self.playlist_name}".')

            playlist_id = self.create_playlist()

        request_data = json.dumps(songs_uris)

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            query,
            data=request_data,
            headers=self.request_headers
        )

        print("Done.")
        return response.json()


if __name__ == '__main__':
    cp = CreatePlaylist("Youtube Liked Songs")
    cp.add_song_to_spotify_playlist()
