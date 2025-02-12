import requests
import os
from dotenv import load_dotenv
import yt_dlp

load_dotenv()

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
APP_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')

RIVALS_GAME_ID = 330654616


url = 'https://api.twitch.tv/helix/clips'

params = {
    "game_id": RIVALS_GAME_ID, 
    "first": 5, 
    "started_at": "2025-02-12T00:00:00Z"
}

headers = { 
    "Authorization": f"Bearer {APP_TOKEN}",
    "Client-Id": CLIENT_ID
}

response = requests.get(url, params=params, headers=headers)

# snippet on how to download a clip

# ydl_opts = {
#         'outtmpl': 'test.mp4',  # Output filename
#         'format': 'mp4'  # Ensure MP4 format
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
#     ydl.download('https://clips.twitch.tv/AwkwardAgileDelicataPeteZaroll-dx7n-9atBk7TYB4Z')

# print(response.json()['data'][0])
