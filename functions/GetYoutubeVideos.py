from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem

import datetime, openai, random, json, requests
from PIL import Image


# READ CONFIGS
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


open_ai_keys = config["OPEN_AI_KEYS"]

ai_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
            

############################################################
def get_video(session, video_url):
    check = session.post("https://yt1s.com/api/ajaxSearch/index", data={"q": video_url, "vt": "home"})
    if check.status_code == 200:
        video_data = check.json()
        if video_data.get('c_status') != 'FAILED':
            return video_data
        else:
            return None
    else:
        return False

def get_this(session, k_url, video_id, self, folder_path):
    check = session.post("https://yt1s.com/api/ajaxConvert/convert", data={"vid": video_id, "k": k_url})
    if check.status_code == 200:
        url_data = check.json()
        if url_data.get("c_status") == "CONVERTED":
            response = session.get(
                url_data.get("dlink"),
                stream=True, 
                headers= {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://yt1s.com/",
                    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
            })

            filename = f"Video_{video_id}.mp3"
            total_size = int(response.headers.get('content-length', 0))
            if response.status_code == 200:
                self.CollectVideoUpdate.emit("downloading mp3 file...")
                with open(folder_path+"/"+filename, 'wb') as file:
                    downloaded_size, progress = 0, 0
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress_1 = round(((downloaded_size / total_size) * 100), 0)
                        if progress != progress_1:
                            try:
                                self.CollectVideoUpdate.emit(f'[ Downloading ] - {progress}%')
                            except:
                                pass
                        progress = progress_1
                    self.CollectVideoUpdate.emit(f'[ Downloading ] - {progress}%')
                return folder_path+"/"+filename
            else:
                return None
        else:
            return None
    else:
        return False


############################################################

def improve_image_quality(input_path, output_path, scale_factor):
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Resize the image
            new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
            
            # Save the enhanced image
            new_img.save(output_path)
            return output_path
    except Exception as e:
        print(f"Error: {e}")


# save to json file
def SaveAsJson(filename, data):
    lyrics = json.loads(json.dumps(data, indent=2))
    with open(filename, 'w') as json_file:
        json.dump(lyrics, json_file)
    return filename

# save youtube cover
def save_image_from_url(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad responses (e.g., 404)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return filename
    except Exception as e:
        return None

# Convert Seconds To Time
def convert_seconds_to_time(seconds):
    delta = datetime.timedelta(seconds=seconds)

    minutes = delta.seconds // 60
    seconds = delta.seconds % 60
    hundredths = delta.microseconds // 10000

    result = f'{minutes:02}:{seconds:02}.{hundredths:02}'    
    return result

# Translate
def translate_to(text, api_key, model):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"Translate this to arabic: '{text}'"},
                {"role": "assistant", "content": "ChatGPT response here..."}
            ],
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
    
    except Exception as error:
        return False

# get video information
def GetVideoInfo(Video_id, thread_self, folder_path):
    video = YouTube("https://www.youtube.com/watch?v="+Video_id)
    YoutubeCoverPath = save_image_from_url(video.thumbnail_url, f'{folder_path}/YoutubeCover.jpg')

    # Example usage
    HighQaulityPath = improve_image_quality(YoutubeCoverPath, f'{folder_path}/YoutubeCover_HighQuality.jpg', 3.0)

    if YoutubeCoverPath != None:
        FramePixmap = QPixmap(YoutubeCoverPath)
        thread_self.CoverViewer.setScaledContents(True)
        thread_self.CoverViewer.setPixmap(FramePixmap)
        thread_self.VideoBackgroundPath.setText(HighQaulityPath)
        thread_self.VideoBackgroundPath2.setText(HighQaulityPath)

    thread_self.VideoSongTitle.setText(f'{video.author} - {video.title}')
    thread_self.song_name_only.setText(f'{video.title}')
    thread_self.ArtistName.setText(f'{video.author}')
    thread_self.SongName_Keyword.setText(f'{video.title}')
    thread_self.ArtistYoutubeChannelLink.setText(f'{video.channel_url}')

    return f"""
title : {video.title}
thumbnail : {YoutubeCoverPath}
channel_url : {video.channel_url}
author : {video.author}
\n\n"""

# get this video
def GetVideo(self, thread_self, Video_id, folder_path, transcript_type):
    lyrics_data = {"lyrics": []}
    information = ""

    information += "[ Getting video information ]\n"
    self.CollectVideoUpdate.emit(information)
    result = GetVideoInfo(Video_id, thread_self, folder_path)
    information += result
    information += "[ Downloading mp3 file ]\n"

    self.CollectVideoUpdate.emit(information)

    session = requests.Session()
    results = get_video(session, "https://www.youtube.com/watch?v="+Video_id)
    if results != None and results != False:
        k_url = results.get('links').get('mp3').get('mp3128').get('k')
        result = get_this(session, k_url, Video_id, self, folder_path)
        if results != None and results != False:
            information += result+"\n\n"
            thread_self.VideoSongPath.setText(f'{result}')
        else:
            information += "No data found.\n\n"
    else:
        information += "No data found.\n\n"

    information += "[ Getting video transcript ]\n"
    self.CollectVideoUpdate.emit(information)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(Video_id, languages=[transcript_type])
        thread_self.lyrics_table.setRowCount(0)
        for idx, caption_text in enumerate(transcript):
            text, start, duration = caption_text.get('text'), caption_text.get('start'), caption_text.get('duration')

            while True:
                key, model = random.choice(open_ai_keys), random.choice(ai_models)
                ar_text = translate_to(text, key, model)
                if ar_text != False:
                    start_time = convert_seconds_to_time(start)
                    lyrics_data["lyrics"].append(
                        {
                            "show_time": start_time,
                            "first_lang": text,
                            "second_lang": ar_text
                        }
                    )
                    self.CollectVideoUpdate.emit(f"{idx}/{len(transcript)} Translated.")

                    # add item to table
                    rowPosition = thread_self.lyrics_table.rowCount()
                    thread_self.lyrics_table.insertRow(rowPosition)

                    item1, item2, item3 = QTableWidgetItem(f'{start_time}'), QTableWidgetItem(text), QTableWidgetItem(ar_text)
                    thread_self.lyrics_table.setItem(rowPosition, 0, item1)
                    thread_self.lyrics_table.setItem(rowPosition, 1, item2)
                    thread_self.lyrics_table.setItem(rowPosition, 2, item3)
                    break

        # save lyrics
        saved = SaveAsJson(f"{folder_path}/lyrics.json", lyrics_data)
        information += f"Transcript saved : {saved}"
        thread_self.DescriptionLyricsPath.setText(f'{saved}')
        thread_self.VideoLyricsPath.setText(f'{saved}')
        
    except Exception as error:
        transcript = None
        information += f"transcript not found\n[ REASON ] - {error}"
    
    self.CollectVideoUpdate.emit(information)

    

