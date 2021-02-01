"""
Module represents the class Youtube that use Youtube API.
"""
import os
import pickle
import googleapiclient.errors
import google_auth_oauthlib.flow
import googleapiclient.discovery


class Youtube:
    """
    A class represents the operations that use Youtube API.

    Attributes
    ----------
    youtube_client_secret : dict
        Youtube client secrets
    manual : bool
        manual or automatic opening browser to get authorization code
    youtube_client :

    """
    def __init__(self, manual_auth=False):
        """
        Constructs all the necessary attributes for the youtube object.

        Parameters
        ----------
            self.youtube_client_secret : dict
                Youtube client secrets
            self.manual : bool
                manual or automatic opening browser to get authorization code
            self.youtube_client : googleapiclient.discovery.Resource
                youtube client object that allows get
                liked videos form Youtube account
        """
        self.youtube_client_secret = "user_secrets/client_secret.json"
        self.manual = manual_auth
        self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self) -> googleapiclient.discovery.Resource:
        """
        Logs Into Youtube and copy from Youtube Data API
        and returns YouTube client using credentials.

        Returns:
            youtube_client (googleapiclient.discovery.Resource):
                youtube client object that allows get
                liked videos form Youtube account
        """
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.youtube_client_secret, scopes)

        if self.manual:
            credentials = flow.run_console()
        else:
            credentials = flow.run_local_server()

            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_videos(self) -> list:
        """
            Returns request response with all liked songs.

            Returns:
                request.execute()["items"] (list): liked items from Youtube
        """
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        return request.execute()["items"]
