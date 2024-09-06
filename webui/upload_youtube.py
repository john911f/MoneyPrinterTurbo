import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes for YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']

# Path to your OAuth 2.0 client secrets file
CLIENT_SECRETS_FILE = 'D:\\DEV\\bot_youtube_client_secret.json'

# Path to the video file you want to upload
VIDEO_FILE = 'D:\\DEV\\MoneyPrinterTurbo\\storage\\tasks\\Epictetus Discourses 2.5.4–5\\final-1.mp4'
PLAYLIST_TITLE = 'Your Playlist Title'
PLAYLIST_DESCRIPTION = 'This is a description of your playlist.'

def add_video_to_playlist(youtube, playlist_id, video_id):
    request_body = {
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',  # Make sure the kind is set correctly
                'videoId': video_id        # The video ID to add to the playlist
            }
        }
    }
    request = youtube.playlistItems().insert(
        part='snippet',
        body=request_body
    )
    request.execute()
    print(f"Video added to playlist {playlist_id}")



def get_or_create_playlist(youtube, title, description):
    # Search for the playlist by title
    request = youtube.playlists().list(
        part='snippet',
        mine=True,
        maxResults=50
    )
    response = request.execute()

    # Check if playlist exists
    for playlist in response.get('items', []):
        if playlist['snippet']['title'] == title:
            return playlist['id']
    
    # Create a new playlist if not found
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': [],
            'defaultLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    request = youtube.playlists().insert(
        part='snippet,status',
        body=request_body
    )
    response = request.execute()
    return response['id']


# Define the upload function
def upload_video(youtube, file_path, title, description, tags, category_id='22'):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'private',  # or 'private' or 'unlisted'
            'selfDeclaredMadeForKids':False
        },
    }
    
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    
    video_id = response['id']
    print(f"Upload complete! Video ID: {video_id}")
    return video_id

def upload_youtube(video_file, title, description, tags):
    # Authenticate and construct the YouTube service object
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    youtube = build('youtube', 'v3', credentials=credentials)

    playlist_id = get_or_create_playlist(youtube, PLAYLIST_TITLE, PLAYLIST_DESCRIPTION)


    video_id = upload_video(
        youtube,
        video_file,
        title=title,
        description=description,
        tags=tags
    )

    add_video_to_playlist(youtube, playlist_id, video_id)

if __name__ == '__main__':
    upload_youtube()
