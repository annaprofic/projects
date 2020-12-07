import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class Youtube:
    def __init__(self):
        self.youtube_client_secret = "client_secret.json"
        self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.youtube_client_secret, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        return request.execute()
