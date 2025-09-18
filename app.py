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
import webbrowser

load_dotenv()

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
APP_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN')

RIVALS_GAME_ID = 330654616

TWITCH_CLIPS_ENDPOINT = 'https://api.twitch.tv/helix/clips'

TAGS = [
    "rivals2",
    "rivals of aether",
    "rivals of aether 2",
    "daily dose of rivals of aether 2",
    "daily soup of rivals of aether 2",
    "rivals 2",
    "daily dose of roa2",
    "roa2",
    "rivals 2", 
    "wrastor", 
    "zetterburn", 
    "kragg", 
    "orcane", 
    "clairen", 
    "olympia", 
    "etalus", 
    "ranno", 
    "absa   "
]


headers = { 
    "Authorization": f"Bearer {APP_TOKEN}",
    "Client-Id": CLIENT_ID
}

def get_top_clips(date: datetime): 
    response = requests.get(
        TWITCH_CLIPS_ENDPOINT, 
        params={
            'game_id': RIVALS_GAME_ID,
            'first': 20,  # fetch 20 so we can pick the best 10
            'started_at': date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),
            'ended_at': date.replace(hour=23, minute=59, second=59, microsecond=59).isoformat()
        }, 
        headers=headers
    )

    if not response.ok:
        print("Failed to fetch clips:", response.text)
        return 

    clip_data = response.json().get('data', [])

    chosen_clips = []
    print("\nReviewing clips. Answer 'y' to include, 'n' to skip. Need 10 total.\n")

    for clip in clip_data:
        if len(chosen_clips) >= 10:
            break  # stop once we have 10
        print(f"\nTitle: {clip['title']}")
        print(f"Streamer: {clip['broadcaster_name']}")
        print(f"URL: {clip['url']}")
        print(f"Duration: {clip['duration']}s")

        # open the clip in default browser
        print(f"\nOpening: {clip['title']} ({clip['broadcaster_name']})")
        print(f"URL: {clip['url']}")
        webbrowser.open(clip['url'])

        choice = input("Include this clip? (y/n): ").strip().lower()
        if choice == 'y':
            chosen_clips.append(clip)

    if len(chosen_clips) < 10:
        print(f"\nWarning: Only {len(chosen_clips)} clips selected. Will continue with fewer than 10.\n")

    # download chosen clips
    for clip in chosen_clips: 
        download_clip(clip['url'], clip['id'])
    
    filepath = combine_clips(chosen_clips)

    title = f"{chosen_clips[0]['title']} ({chosen_clips[0]['broadcaster_name']}) - Rivals of Aether 2 Highlights {date.strftime('%m/%d')}"
    description=f"Top Rivals of Aether 2 Clips from {date.strftime('%m/%d/%Y')}\n\n"

    offset = 0 
    for clip in chosen_clips: 
        description += f"{int(offset / 60):02}:{int(offset % 60):02} {clip['title']} - twitch.tv/{clip['broadcaster_name']}\n"
        offset += clip['duration']

    description += "\nLike and Subscribe\n\n"
    description += "All clips are retrieved, edited, and credited by a program. If you have concerns or would like content removed, please comment and I will do so. "

    # youtube does not support angle brackets in description
    description = re.sub(r'[<>]', '', description)

    with open('resume.json', 'w') as jsonFile: 
        json.dump({'description': description, 'title': title}, jsonFile)

    upload_video(filepath, title, description, tags=TAGS)
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
    upload_video(filepath, title, description, tags=TAGS)
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