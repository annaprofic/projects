from projects.spotify_playlist.user_secrets.secrets import spotify_user_id, spotify_user_token
import json
import requests


class Spotify:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_user_token
        self.request_headers = {
            "Content_Type": "application/json",
            "Authorization": f"Bearer {self.spotify_token}"
        }

    def get_song_uri(self, *args):
        query = f'https://api.spotify.com/v1/search?q={args}&type=track&limit=20&offset=0'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        songs_list = response.json()["tracks"]["items"]
        return songs_list[0]["uri"]

    def get_all_playlists_info(self):
        query = 'https://api.spotify.com/v1/me/playlists'
        response = requests.get(
            query,
            headers=self.request_headers
        )

        return response.json()

    def get_playlists_items(self, playlist_id):
        query = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        return [item["track"]["uri"] for item in response.json()["items"]]

    def check_for_playlist_existent(self, playlist_name):
        return any(tag['name'] == playlist_name for tag in self.get_all_playlists_info()['items'])

    def get_existing_playlist_id(self, playlist_name):
        return [curr_playlist['id'] for curr_playlist in self.get_all_playlists_info()['items']
                if curr_playlist['name'] == playlist_name][0]

    def create_playlist(self, playlist_name):
        request_body = json.dumps({
            "name": playlist_name,
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

    def add_items_to_playlist(self, playlist_name, songs):

        playlist_items = {}

        if self.check_for_playlist_existent(playlist_name):
            print(f'\n[spotify] playlist "{playlist_name}" is already exist.')
            print(f'[spotify] getting playlist "{playlist_name}" id.')
            playlist_id = self.get_existing_playlist_id(playlist_name)
            playlist_items = set(self.get_playlists_items(playlist_id))
        else:
            print(f'\n[spotify] creating playlist "{playlist_name}"')
            playlist_id = self.create_playlist(playlist_name)

        songs_uris = []
        for song, info in songs.items():
            song_uri = info['spotify_uri']
            if song_uri not in playlist_items:
                songs_uris.append(song_uri)

        if songs_uris:
            request_data = json.dumps(songs_uris)
            query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            requests.post(
                query,
                data=request_data,
                headers=self.request_headers
            )
            print("\nAll founded songs from Youtube liked videos "
                  "are now in your Spotify playlist.")

        else:
            print("\nAll founded songs from Youtube liked videos "
                  "has already been added to your Spotify playlist.")
