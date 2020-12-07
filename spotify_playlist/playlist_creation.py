from projects.spotify_playlist.utilities import text_normalizing as tn
from projects.spotify_playlist.spotify import Spotify
from projects.spotify_playlist.youtube import Youtube
import youtube_dl


def songs_name_normalizing(*args):
    return [tn.normalize(arg) for arg in args]


class Playlist:

    def __init__(self):
        self.spotify = Spotify()
        self.youtube = Youtube()

    def get_all_songs_info(self):

        liked_songs_info = {}

        # collect each video and get important information
        for item in self.youtube.get_liked_videos()["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = f"https://www.youtube.com/watch?v={item['id']}"

            # use youtube_dl to collect the song name & artist name
            video_url = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            song_name, artist_name = songs_name_normalizing(video_url["track"], video_url["artist"])

            try:
                spotify_song_uri = self.spotify.get_song_uri(song_name, artist_name)
                liked_songs_info[video_title] = {"video_url": video_url,
                                                 "song_name": song_name,
                                                 "song_artist": artist_name,
                                                 "spotify_uri": spotify_song_uri}

                print("[spotify] song", artist_name, "-", song_name, "has been found")

            except IndexError:
                print("[spotify] ERROR we couldn't find this song", artist_name, "-", song_name)

            except KeyError:
                print("[spotify] your Spotify token has been expired, please update your token")
                exit(1)

        return liked_songs_info

    def create(self, playlist_name):
        self.spotify.add_items_to_playlist(playlist_name, self.get_all_songs_info())


if __name__ == '__main__':
    playlist = Playlist()
    playlist.create("Youtube Liked Songs")
