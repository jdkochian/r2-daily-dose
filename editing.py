from moviepy import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

clip_paths = ['ImpossibleCourageousDoveRedCoat-qPs0f8_xBR5d7S_y.mp4', 'PiercingSavoryCougarAsianGlow-g6GvcBSCYaPsyJS2.mp4']

# snippet for stitching together the clips and adding text

clips = [VideoFileClip(f'./clips/{video}') for video in clip_paths]

for i, clip in enumerate(clips): 
    clip = clip.resized((1920, 1080))

    # todo: pass in the clip title, put in bottom left corner, figure out how to do multiline with the channel
    text = TextClip(font='Courier', text=clip_paths[i].split('.')[0], font_size=150, color='white', stroke_color='black', stroke_width=5, horizontal_align='center', vertical_align='center', duration=2.5)
    clips[i] = CompositeVideoClip([clip, text])


final_video = concatenate_videoclips(clips, method='compose') 
final_video.write_videofile('test.mp4')
