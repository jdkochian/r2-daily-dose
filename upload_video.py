import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_PATH = "token.pickle"
CLIENT_SECRET_FILE = "client_secret.json"


def run_new_oauth_flow():
    """Force a new OAuth login flow."""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    return flow.run_local_server(port=8080)


def authenticate_youtube():
    """Authenticate and return credentials, refreshing or reauthing if needed."""
    creds = None

    # Load credentials if available
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                print("⚠️ Refresh failed, opening new OAuth flow...")
                creds = run_new_oauth_flow()
        else:
            creds = run_new_oauth_flow()

        # Save credentials back (new or refreshed)
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return creds


def upload_video(file_path, title, description, tags):
    """Upload a video to YouTube."""
    creds = authenticate_youtube()

    # Refresh before each request just to be safe
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)
        except RefreshError:
            print("⚠️ Refresh failed mid-request, reopening OAuth flow...")
            creds = run_new_oauth_flow()
            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)

    

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "20"  # Gaming category
            },
            "status": {"privacyStatus": "public"}  # or "private", "unlisted"
        },
        media_body=MediaFileUpload(file_path, resumable=True)
    )

    print("🎥 Attempting upload...")

    response = request.execute()
    print("✅ Uploaded video ID:", response["id"])

