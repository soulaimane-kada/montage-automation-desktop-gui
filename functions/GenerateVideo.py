import json, sys
from PIL import Image
import moviepy.config as cfg
from googletrans import Translator

from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


# translate text
translator = Translator()
def translate_to_arabic(text, dest):
    while True:
        try:
            translated_text = translator.translate(text, dest=dest).text
            break
        except Exception as error:
            pass
    return translated_text

# USE 4 COREs
cfg.n_threads = 4

#################
english_title_font, english_title_font_size = "assets/fonts/Caveat/Caveat-Bold.ttf", 60
english_album_font, english_album_font_size = "assets/fonts/Caveat/Caveat-Bold.ttf", 45

english_cover_font = "assets/fonts/Gagalin/TTF/Gagalin-Regular.ttf"
arabic_cover_font = "assets/fonts/Madani/Madani Arabic Regular.ttf"


def convert_to_seconds(length):
    time_parts = length[1:-1].split(':')
    minutes = int(time_parts[0])
    seconds = float(time_parts[1])
    total_seconds = minutes * 60 + seconds
    return total_seconds

def get_lyrics(lyrics_file):
    with open(lyrics_file, "r", encoding='utf-8') as file:
        timestamps = []
        lyrics = []
        for line in file:
            line = line.strip()
            if line.startswith("[") and "]" in line:
                timestamp, lyric = line.split("]", 1)
                timestamp += "]"
                lyrics.append(lyric.strip())
                timestamps.append(timestamp)

        data = []
        for i in range(len(timestamps) - 1):
            start = convert_to_seconds(f'{timestamps[i]}')
            end = convert_to_seconds(f'{timestamps[i + 1]}')
            text = lyrics[i]
            data.append({
                "text": text,
                "starts": start,
                "ends": end
            })

        # Handle the last timestamp and lyric separately
        last_start = convert_to_seconds(f'{timestamps[-1]}')
        last_end = last_start  # Use the same timestamp as the start
        last_text = lyrics[-1]
        data.append({
            "text": last_text,
            "starts": last_start,
            "ends": last_end
        })

        # Print the resulting JSON data
        lyrics = json.loads(json.dumps(data, indent=2))
    return lyrics

import json

# Dummy implementation of convert_to_seconds
def convert_to_seconds_2(time_string):
    return float(time_string.split(":")[0]) * 60 + float(time_string.split(":")[1])

def get_lyrics_json(lyrics_file):
    print (lyrics_file)
    with open(lyrics_file, "r", encoding='utf-8') as file:
        data = json.load(file)

        lyrics = data["lyrics"]
        result = []
        for i in range(len(lyrics) - 1):
            start = convert_to_seconds_2(f'{lyrics[i]["show_time"]}')
            end = convert_to_seconds_2(f'{lyrics[i+1]["show_time"]}')
            text = lyrics[i]["first_lang"] + lyrics[i]["second_lang"]
            result.append({
                "text": text,
                "starts": start,
                "ends": end,
                "first_lang": lyrics[i]["first_lang"],
                "second_lang": lyrics[i]["second_lang"]
            })
        
        # Handle the last timestamp and lyric separately
        last_start = convert_to_seconds_2(f'{lyrics[-1]["show_time"]}')
        last_end = last_start  # Use the same timestamp as the start
        last_text = lyrics[-1]["first_lang"] + lyrics[-1]["second_lang"]
        result.append({
            "text": last_text,
            "starts": last_start,
            "ends": last_end,
            "first_lang": lyrics[-1]["first_lang"],
            "second_lang": lyrics[-1]["second_lang"]
        })
        
        lyrics = json.loads(json.dumps(result, indent=2))
        return lyrics
    
# generate frame - 1080p
def generate_frame_1080p(self, background_path, logo_path, song_title, song_album, Transparant):
    global english_title_font, english_title_font_size, english_album_font, english_album_font_size
    
    # set background
    bg_image = ImageClip(background_path)
    
    if Transparant == "5%":
        bg_tr = ImageClip("assets/tr_5.png")
    elif Transparant == "10%":
        bg_tr = ImageClip("assets/tr_10.png")
    elif Transparant == "15%":
        bg_tr = ImageClip("assets/tr_15.png")
    elif Transparant == "20%":
        bg_tr = ImageClip("assets/tr_20.png")
    elif Transparant == "25%":
        bg_tr = ImageClip("assets/tr_25.png")
    elif Transparant == "30%":
        bg_tr = ImageClip("assets/tr_30.png")
    elif Transparant == "35%":
        bg_tr = ImageClip("assets/tr_35.png")
    elif Transparant == "40%":
        bg_tr = ImageClip("assets/tr_40.png")
    elif Transparant == "45%":
        bg_tr = ImageClip("assets/tr_45.png")
    elif Transparant == "50%":
        bg_tr = ImageClip("assets/tr_50.png")
    elif Transparant == "55%":
        bg_tr = ImageClip("assets/tr_55.png")
    elif Transparant == "60%":
        bg_tr = ImageClip("assets/tr_60.png")
    elif Transparant == "65%":
        bg_tr = ImageClip("assets/tr_65.png")
    elif Transparant == "70%":
        bg_tr = ImageClip("assets/tr_70.png")
    elif Transparant == "75%":
        bg_tr = ImageClip("assets/tr_75.png")
    elif Transparant == "80%":
        bg_tr = ImageClip("assets/tr_80.png")
    elif Transparant == "85%":
        bg_tr = ImageClip("assets/tr_85.png")
    elif Transparant == "90%":
        bg_tr = ImageClip("assets/tr_90.png")
    elif Transparant == "95%":
        bg_tr = ImageClip("assets/tr_95.png")
    elif Transparant == "100%":
        bg_tr = ImageClip("assets/tr_100.png")
        
    # set logo white background
    logo_backgound = ImageClip("assets/white.jpg")
    logo_backgound = logo_backgound.resize((190, 190))
    left, top, right, bottom = 25, 25, 0, 0
    logo_backgound = logo_backgound.set_position((left, top))

    # set album logo
    logo = ImageClip(logo_path)
    logo = logo.resize((180, 180))
    left, top, right, bottom = 30, 30, 0, 0
    logo = logo.set_position((left, top))

    # set song title & album name
    label1 = TextClip(song_title, fontsize=english_title_font_size, color='white', font=english_title_font)
    label2 = TextClip(song_album, fontsize=english_album_font_size, color='white', font=english_album_font)

    label1_pos = (left + logo.w + 20, top + 15)
    label2_pos = (left + logo.w + 25, top + label1.h + 30)
    
    label1 = label1.set_position(label1_pos)
    label2 = label2.set_position(label2_pos)

    # build the frame & save
    try:
        self.video_update_box.emit('building frame...')
    except:
        pass
    
    video = CompositeVideoClip([bg_image.resize(height=1080).set_position('center'), bg_tr, logo_backgound, logo, label1, label2], size=(1920, 1080))
    video.save_frame('assets/frame.png')
    try:
        self.video_update_box.emit('Frame is ready')
    except:
        pass
    return [bg_image, logo_backgound, logo, label1, label2, bg_tr]


def generate_video(background_path, logo_path, VideoSong, VideoLyrics, song_title, song_album, Translate, VideoQuality, VideoLength, VideoFontType, SavePath, lyrics_type, Transparant):

    #if VideoLength == "1080p":
    #    pass
    
    font_type, font_size = None, None
    if VideoFontType == "Caveat Font ( English )":
        font_type = "assets/fonts/Caveat/Caveat-Bold.ttf"
        font_size = 95
    elif VideoFontType == "Cairo Font ( Arabic/English )":
        font_type = "assets/fonts/arabic/Cairo-Bold.ttf"
        font_size = 60
    elif VideoFontType == "Cairo Font - Extra Bold ( Arabic/English )":
        font_type = "assets/fonts/arabic/Cairo-ExtraBold.ttf"
        font_size = 60
    elif VideoFontType == "Cairo Font - Black ( Arabic/English )":
        font_type = "assets/fonts/arabic/Cairo-Black.ttf"
        font_size = 60
    elif VideoFontType == "Tajawal Font - Bold ( Arabic/English )":
        font_type = "assets/fonts/Tajawal/Tajawal-Bold.ttf"
        font_size = 60
    elif VideoFontType == "Tajawal Font - Exrta Bold ( Arabic/English )":
        font_type = "assets/fonts/Tajawal/Tajawal-ExtraBold.ttf"
        font_size = 60
    
    video_info = generate_frame_1080p("", background_path, logo_path, song_title, song_album, Transparant)
    
    # get lyrics
    if lyrics_type == "lrc_type":
        lyrics = get_lyrics(VideoLyrics)
        
        # add lyrics to video
        lyrics_clips, lyrics_text = [], ''
        for line in lyrics:
            # to arabic and add
            if Translate == "without translation":
                if "{LYRICS_SPLIT}" in line.get("text"):
                    no_translate = (line.get("text")).split("{LYRICS_SPLIT}")
                    line_text = no_translate[0].strip() + "\n" + no_translate[1].strip()
                else:
                    line_text = line.get("text")
                if "{space}" in line_text:
                    no_translate = line_text.split("{space}")
                    line_text = no_translate[0].strip() + "\n" + no_translate[1].strip()
                else:
                    line_text = line_text
        
            elif Translate.startswith('translate'):
                #print ('Translating now...')
                if Translate == "translate to arabic":
                    translate_code = "ar"
                elif Translate == "translate to english":
                    translate_code = "en"
                elif Translate == "translate to spanish":
                    translate_code = "es"
        
                if "{space}" in line.get("text"):
                    to_translate = (line.get("text")).split("{space}")
                    part_1, part_2 = translate_to_arabic(to_translate[0].strip(), translate_code), translate_to_arabic(to_translate[1].strip(), translate_code)
                    line_text = to_translate[0] + "\n" + to_translate[1] + "\n" + part_1 + "\n" + part_2
                else:
                    arabic_text = translate_to_arabic(line.get("text"), translate_code)
                    line_text = line.get("text").strip() + "\n" + arabic_text.strip()
        
            text = TextClip(line_text, fontsize=font_size, font=font_type, color='white')
            text_clip = text.set_position('center').set_start(float(line.get("starts"))).set_duration(round((line.get("ends") - line.get("starts")), 2))
            lyrics_clips.append(text_clip)
                
    if lyrics_type == "json_type":
        lyrics_clips = []
        lyrics_data = get_lyrics_json(VideoLyrics)
    
        for line in lyrics_data:
            if "{SPACE}" in line.get('first_lang'):
                first_lang = line.get('first_lang').replace("{SPACE}", "\n")
            else:
                first_lang = line.get('first_lang')
            if "{SPACE}" in line.get('second_lang'):
                second_lang = line.get('second_lang').replace("{SPACE}", "\n")
            else:
                second_lang = line.get('second_lang')

            line_text = first_lang + "\n" + second_lang
            #line_text = line.get('first_lang') + "\n" + line.get('second_lang')
            text = TextClip(line_text, fontsize=font_size, font=font_type, color='white')
            text_clip = text.set_position('center').set_start(float(line.get("starts"))).set_duration(round((line.get("ends") - line.get("starts")), 2))
            lyrics_clips.append(text_clip)

    
    #build the video
    print ("building video...")
    full_bg = CompositeVideoClip([video_info[0].resize(height=1080).set_position('center'), video_info[5].resize(height=1080)])
    full_bg.save_frame('assets/frame.png')
    png_image = Image.open("assets/frame.png")
    rgb_image = png_image.convert('RGB')
    rgb_image.save("assets/output.jpg")
    bg_image = ImageClip('assets/output.jpg')

    video = CompositeVideoClip([bg_image, video_info[1], video_info[2], video_info[3], video_info[4]] + lyrics_clips, size=(1920, 1080))
    #video = CompositeVideoClip([video_info[0].resize(height=1080).set_position('center'), video_info[1], video_info[2], video_info[3], video_info[4]] + lyrics_clips, size=(1920, 1080))
    
    # Load the audio file and add it
    audio = AudioFileClip(VideoSong)
    
    # Write the video to a file
    if VideoLength == "audio length":
        video = video.set_duration(audio.duration)
    else:
        video = video.set_duration(int(VideoLength))
    
    video = video.set_audio(audio)
    video.write_videofile(SavePath, fps=30, threads=4)
    
# cut video
def cut_video(VideoPath, start_time, end_time, SavePath): 
    # Split the time string into its components and convert them to integers
    hours, minutes, seconds = map(int, start_time.split(':'))
    start_time = (hours * 3600) + (minutes * 60) + seconds
    
    hours, minutes, seconds = map(int, end_time.split(':'))
    end_time = (hours * 3600) + (minutes * 60) + seconds

    # Load the input video
    input_clip = VideoFileClip(VideoPath)
    output_clip = input_clip.subclip(float(start_time), float(end_time))

    # Save the output clip to a file
    output_clip.write_videofile(SavePath)
        
# make cover
def make_cover_now(self, background_path, song_name, second_word, size_1, size_2, SavePath, Transparnt):
    bg_image = ImageClip(background_path)

    if Transparnt == "5%":
        bg_tr = ImageClip("assets/tr_5.png")
    elif Transparnt == "10%":
        bg_tr = ImageClip("assets/tr_10.png")
    elif Transparnt == "15%":
        bg_tr = ImageClip("assets/tr_15.png")
    elif Transparnt == "20%":
        bg_tr = ImageClip("assets/tr_20.png")
    elif Transparnt == "25%":
        bg_tr = ImageClip("assets/tr_25.png")
    elif Transparnt == "30%":
        bg_tr = ImageClip("assets/tr_30.png")
    elif Transparnt == "35%":
        bg_tr = ImageClip("assets/tr_35.png")
    elif Transparnt == "40%":
        bg_tr = ImageClip("assets/tr_40.png")
    elif Transparnt == "45%":
        bg_tr = ImageClip("assets/tr_45.png")
    elif Transparnt == "50%":
        bg_tr = ImageClip("assets/tr_50.png")
    elif Transparnt == "55%":
        bg_tr = ImageClip("assets/tr_55.png")
    elif Transparnt == "60%":
        bg_tr = ImageClip("assets/tr_60.png")
    elif Transparnt == "65%":
        bg_tr = ImageClip("assets/tr_65.png")
    elif Transparnt == "70%":
        bg_tr = ImageClip("assets/tr_70.png")
    elif Transparnt == "75%":
        bg_tr = ImageClip("assets/tr_75.png")
    elif Transparnt == "80%":
        bg_tr = ImageClip("assets/tr_80.png")
    elif Transparnt == "85%":
        bg_tr = ImageClip("assets/tr_85.png")
    elif Transparnt == "90%":
        bg_tr = ImageClip("assets/tr_90.png")
    elif Transparnt == "95%":
        bg_tr = ImageClip("assets/tr_95.png")
    elif Transparnt == "100%":
        bg_tr = ImageClip("assets/tr_100.png")

    # set song title & album name
    label1 = TextClip(song_name, fontsize=int(size_1), color='yellow', font=english_cover_font)
    label2 = TextClip(second_word, fontsize=int(size_2), color='white', font=arabic_cover_font)

    label2_pos = ('center', 850)
    
    label1 = label1.set_position('center')
    label2 = label2.set_position(label2_pos)

    # build the frame & save
    try:
        self.video_update_box.emit('building cover...')
    except:
        pass

    video = CompositeVideoClip([bg_image.resize(height=1080).set_position('center'), bg_tr.resize(height=1080), label1, label2], size=(1920, 1080))
    video.save_frame('assets/frame.png')
    video.save_frame(SavePath)
    
    try:
        self.video_update_box.emit('cover is ready')
    except:
        pass
    return SavePath
    
    
    

    
# Generate video
try:
    function_name = sys.argv[1]
    args = sys.argv[2:]
    function = (lambda f: f(*args))(globals()[function_name])
        
except Exception as error:
    if str(error) != "list index out of range":
        print (error)