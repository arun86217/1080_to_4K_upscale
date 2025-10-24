from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os, sys

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_youtube_service():
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

def upload(video_file):
    youtube = get_youtube_service()
    title = os.path.basename(video_file).replace("_4k.mp4","")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": "Auto-uploaded 4K gameplay"},
            "status": {"privacyStatus": "unlisted"}
        },
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")
    print("Upload complete:", response.get("id"))
