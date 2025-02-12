import requests
import os
from dotenv import load_dotenv
import yt_dlp
from datetime import datetime, timedelta, timezone

load_dotenv()

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
APP_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')

RIVALS_GAME_ID = 330654616

TWITCH_CLIPS_ENDPOINT = 'https://api.twitch.tv/helix/clips'

headers = { 
    "Authorization": f"Bearer {APP_TOKEN}",
    "Client-Id": CLIENT_ID
}

def get_top_clips(date : datetime): 
    response = requests.get(TWITCH_CLIPS_ENDPOINT, params={'game_id': RIVALS_GAME_ID, 'first': 5, 'started_at': date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()}, headers=headers)
    if (response.ok): 
        clip_data = response.json()['data']
        # todo: parallelize this
        for clip in clip_data: 
            download_clip(clip['url'], clip['id'])

        # todo: stitch clips together, add text with clip title and creator, upload
    
def download_clip(clip_url : str, clip_id): 
    ydl_opts = {
        'outtmpl': f'clips/{clip_id}.mp4', 
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        ydl.download(clip_url)

yesterday = datetime.now(timezone.utc) - timedelta(days=1)
# get_top_clips(yesterday)