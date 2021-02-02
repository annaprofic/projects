"""
Module to represent the class that creates the playlist with youtube liked song on Spotify.
"""
import sys
import youtube_dl
from projects.spotify_playlist.utilities import text_normalizing as tn
from projects.spotify_playlist.spotify import Spotify
from projects.spotify_playlist.youtube import Youtube


def songs_name_normalizing(*args) -> list:
    """
        Normalizes song names by denoising text and removing punctuation.

        Arguments:
            *args (tuple): text to normalize (songs names)
        Returns:
            normalized text with songs names
    """
    return [tn.normalize(str(arg)) for arg in args]


class Playlist:
    """
    A class that used to create the playlist with youtube
    liked song on Spotify.

    ...

    Attributes
    ----------
    spotify : Spotify object
        Spotify object that helps to get class attributed and methods
    youtube : Youtube object
        Youtube object that helps to get class attributed and methods

    Methods
    -------
    get_all_songs_info() -> dict:
        Grabs all liked videos & create a dictionary of important song information.

    def create(playlist_name) -> None:
        Adds all items to a playlist.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for adding items from
        Youtube liked songs to Spotify playlist.

        Parameters
        ----------
            self.spotify : Spotify object
                object responsible for connection with Spotify API
            self.youtube : Youtube object
                object responsible for connection with Youtube API

        """
        self.spotify = Spotify()
        self.youtube = Youtube()

    def get_all_songs_info(self) -> dict:
        """
        Grabs all liked videos & create a dictionary of
        important song information such as video_url, song_name,
        song_artist, spotify_uri.

        Returns:
            liked_songs_info (dict): dictionary with information about the songs
        """

        liked_songs_info = {}
        # collect each video and get important information
        for item in self.youtube.get_liked_videos():
            video_title = item["snippet"]["title"]
            youtube_url = f"https://www.youtube.com/watch?v={item['id']}"
            print("_____________________________________________"
                  "______________________________________________")

            # use youtube_dl to collect the song name & artist name
            try:
                video_url = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            except youtube_dl.utils.DownloadError:
                print(f'\033[91m[youtube] Something went wrong with video "{video_title}".\n'
                      f'[youtube] Please, remove it from your list and try again.\033[0m')
                sys.exit()

            song_name, artist_name = video_url["track"], video_url["artist"]

            # collect all information about song and get spotify uri
            try:
                if not (song_name and artist_name):
                    artist_name, song_name = "Unknown artist", "Unknown track"
                    raise IndexError

                spotify_song_uri = self.spotify.get_song_uri(songs_name_normalizing(song_name,
                                                                                    artist_name))
                liked_songs_info[video_title] = {"video_url": video_url,
                                                 "song_name": song_name,
                                                 "song_artist": artist_name,
                                                 "spotify_uri": spotify_song_uri}

                print("[spotify] song", artist_name, "-", song_name, "has been found.")

            except IndexError:
                print("\033[91m[spotify] WARNING we couldn't find this song.",
                      artist_name, "-", song_name, '\033[0m')
                continue

            except KeyError:
                print("\033[91m[spotify] your Spotify token has been expired, "
                      "please update your token.\033[0m")
                sys.exit()

        return liked_songs_info

    def create(self, playlist_name) -> None:
        """
        Adds all items to a playlist.

        Arguments:
            playlist_name (str): name of the playlist that should be created
        """
        self.spotify.add_items_to_playlist(playlist_name, self.get_all_songs_info())


if __name__ == '__main__':
    playlist = Playlist()
    playlist.create("Youtube Liked Songs")
