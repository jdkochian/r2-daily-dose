import json
import requests
import os
from dotenv import load_dotenv
import yt_dlp
from datetime import datetime, timedelta
import pytz
from editing import combine_clips
from upload_video import upload_video
import re

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
    response = requests.get(TWITCH_CLIPS_ENDPOINT, params={'game_id': RIVALS_GAME_ID, 'first': 10, 'started_at': date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(), 'ended_at': date.replace(hour=23, minute=59, second=59, microsecond=59).isoformat()}, headers=headers)
    if (response.ok): 
        clip_data = response.json()['data']

        # todo: parallelize this
        for clip in clip_data: 
            download_clip(clip['url'], clip['id'])
        
        filepath = combine_clips(clip_data)
        # filepath = 'test.mp4'

        title = f"{clip_data[0]['title']} ({clip_data[0]['broadcaster_name']}) - Rivals of Aether 2 Highlights {date.strftime('%m/%d')}"
        description=f"""Top Rivals of Aether 2 Clips from {date.strftime('%m/%d/%Y')}\n\n"""

        offset = 0 
        for clip in clip_data: 
            description += f"""{int(offset / 60):02}:{int(offset % 60):02} {clip['title']} - twitch.tv/{clip['broadcaster_name']}\n"""
            offset += clip['duration']

        description += "\nLike and Subscribe\n\n"
        description += "All clips are retrieved, edited, and credited by a program. If you have concerns or would like content removed, please comment and I will do so. "

        # youtube does not support angle brackets in description
        description = re.sub(r'[<>]', '', description)

        with open('resume.json', 'w') as jsonFile: 
            json.dump({'description': description, 'title': title}, jsonFile)

        upload_video(filepath, title, description, ['rivals2'])
        cleanup()

def download_clip(clip_url : str, clip_id): 
    ydl_opts = {
        'outtmpl': f'clips/{clip_id}.mp4', 
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        ydl.download(clip_url)

def upload_from_resumable(): 
    filepath = 'test.mp4'
    with open('resume.json', 'r') as jsonFile: 
        data = json.load(jsonFile)

    description = data['description']
    title = data['title']
    upload_video(filepath, title, description, ['rivals2'])
    cleanup()

def cleanup(): 
    for filename in os.listdir('./clips'):
        file_path = os.path.join('./clips', filename)
        if os.path.isfile(file_path):  # extra safe check
            os.remove(file_path)
    os.remove('./test.mp4')

est = pytz.timezone("America/New_York")
yesterday = datetime.now(est) - timedelta(days=1)


get_top_clips(yesterday)
# upload_from_resumable()
# print(yesterday)