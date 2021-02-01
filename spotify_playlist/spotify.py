"""
Module represents the class Spotify that use Spotify API.
"""
import json
import requests
from projects.spotify_playlist.user_secrets.secrets import spotify_user_id, spotify_user_token


class Spotify:
    """
    A class represents the operations that use Spotify API.

    Attributes
    ----------
    user_id : str
        Spotify user id
    spotify_token : str
        Spotify token
    request_headers : dict
        headers used in the most of requests

    Methods
    -------
    get_song_uri(*args) -> str:
        Searches for the song through Spotify API and returns its first result.

    get_all_playlists_info() -> dict:
        Returns dict with all information provided by API about user's playlists.

    get_playlists_items(playlist_id: str) -> str:
        Returns all item's uris from the playlist.

    check_for_playlist_existent(playlist_name: str) -> bool:
        Checks if playlist with name given as an argument exists.

    get_existing_playlist_id(playlist_name: str) -> str:
        Returns the playlist with name given as an argument.

    create_playlist(self, playlist_name: str) -> str:
        Creates playlist.

    add_items_to_playlist(playlist_name: str, songs: dict) -> None:
        Checks if playlist with given name exists. If yes - gets playlist id
        and items from this playlist. If not - creates new playlist and gets its id.

    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the spotify object.

        Parameters
        ----------
            self.user_id : str
                Spotify user id
            self.spotify_token : str
                Spotify token
            self.request_headers : dict
                headers used in the most of requests
        """
        self.user_id = spotify_user_id
        self.spotify_token = spotify_user_token
        self.request_headers = {
            "Content_Type": "application/json",
            "Authorization": f"Bearer {self.spotify_token}"
        }

    def get_song_uri(self, *args) -> str:
        """
        Searches for the song through Spotify API and returns its first result.

        Arguments:
            args (list): song name and artist name
        Returns:
            songs_list[0]["uri"] (str): the first song uri
        """
        query = f'https://api.spotify.com/v1/search?q={args}&type=track&limit=20&offset=0'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        songs_list = response.json()["tracks"]["items"]
        return songs_list[0]["uri"]

    def get_all_playlists_info(self) -> dict:
        """
        Returns dict with all information provided by API about user's playlists.

        Returns:
            response.json() {dict} -- request response, dictionary with
                                      information about the playlists
        """
        query = 'https://api.spotify.com/v1/me/playlists'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        return response.json()

    def get_playlists_items(self, playlist_id: str) -> str:
        """
        Returns all item's uris from the playlist.

        Arguments:
            playlist_id {str): id of the playlist
        Returns:
            items_uris {list} -- list with song's uris from playlist
        """
        query = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        response = requests.get(
            query,
            headers=self.request_headers
        )
        items_uris = [item["track"]["uri"] for item in response.json()["items"]]
        return items_uris

    def check_for_playlist_existent(self, playlist_name: str) -> bool:
        """
        Checks if playlist with name given as an argument exists.

        Arguments:
            playlist_name {str} -- name of the playlist
        Returns:
            True - if user already has playlist with this name, False if not
        """
        return any(tag['name'] == playlist_name for tag in self.get_all_playlists_info()['items'])

    def get_existing_playlist_id(self, playlist_name: str) -> str:
        """
        Searches for playlist with name given as an argument
        through all user's playlists and returns that playlist.

        Arguments:
            playlist_name {str} -- name of the playlist
        Returns:
            id of the playlist which has the name as given in arguments
        """
        return [curr_playlist['id'] for curr_playlist in self.get_all_playlists_info()['items']
                if curr_playlist['name'] == playlist_name][0]

    def create_playlist(self, playlist_name: str) -> str:
        """
        Creates playlist.

        Arguments:
            playlist_name {str} -- name of the playlist that will be created
        Returns:
            response.json()["id"] {str} -- id of the created playlist
        """
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

    def add_items_to_playlist(self, playlist_name: str, songs: dict) -> None:
        """
        Checks if playlist with given name exists. If yes - gets playlist id
        and items from this playlist. If not - creates new playlist and gets its id.

        Adds iteratively items from dictionary to playlist if it doesn't have ones.

        Arguments:
            playlist_name {str} -- name of the playlist
        """

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
        for _, info in songs.items():
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
