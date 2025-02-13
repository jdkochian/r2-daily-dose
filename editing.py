from moviepy import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def combine_clips(clip_data): 
    clips = [VideoFileClip(f"./clips/{clip['id']}.mp4") for clip in clip_data]

    for i, clip in enumerate(clips): 
        clip = clip.resized((1920, 1080))
        # todo: multiline with title and channel
        text = TextClip(font='Courier', text=f"twitch.tv/{clip_data[i]['broadcaster_name']}", font_size=100, color='white', stroke_color='purple', stroke_width=5, horizontal_align='center', vertical_align='center', duration=2.5).with_position(('left', 'bottom'))

        clips[i] = CompositeVideoClip([clip, text]).with_audio(clips[i].audio)

    final_video = concatenate_videoclips(clips, method='compose')
    final_video.write_videofile('test.mp4', audio=True, audio_codec='aac')