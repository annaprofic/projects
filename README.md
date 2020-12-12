## Spotify playlist creation that based on Youtube liked songs.

spotify_playlist/

a simple script that takes liked videos from your account on Youtube, and generates a Spotify playlist based on these songs.

## Table of Contents
* [Technologies](#Technologies)
* [Setup](#LocalSetup)


## Technologies
* [Youtube Data API v3]
* [Spotify Web API]
* [Youtube_dl v2020.12.12]
* [Requests library v2.25.0]

## LocalSetup
1) to install dependencies run this command:
`pip3 install -r requirements.txt`

2) Collect You Spotify User ID and Oauth Token From Spotfiy and add it to secrets.py file
    * your User ID is just your Spotify **Username**, that you can find here [Account Overview] 
    * to collect Oauth Token, visit this url: [Get Oauth] and click the **Get Token** button

3) Enable Oauth For Youtube to download the client_secrets.json   
    * this guide will help with this part [Set Up Youtube Oauth]

4) Run the File  
`python3 playlist_creation.py`   
    * when see this: `Please visit this URL to authorize this application: <some long url>`
    * click on this link and log into your Google Account 
    * allow this program use your Youtube account to collect the `authorization code`
 


   [Youtube Data API v3]: <https://developers.google.com/youtube/v3>
   [Spotify Web API]: <https://developer.spotify.com/documentation/web-api/>
   [Requests library v2.25.0]: <https://requests.readthedocs.io/en/master/>
   
   [Account Overview]: <https://www.spotify.com/us/account/overview/> 
   [Get Oauth]: <https://developer.spotify.com/console/post-playlists/>
   
   [Set Up Youtube Oauth]: <https://developers.google.com/youtube/v3/getting-started/>
   [Youtube Video]:<https://www.youtube.com/watch?v=7J_qcttfnJA/>
   [Youtube_dl v2020.12.12]:<https://github.com/ytdl-org/youtube-dl/> 