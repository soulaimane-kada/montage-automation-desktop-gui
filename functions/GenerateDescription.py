from googletrans import Translator
import json


# translator session
translator = Translator()


####################################
# translate text
def translate_to_arabic(text, dest):
    while True:
        try:
            translated_text = translator.translate(text, dest=dest).text
            break
        except Exception as error:
            pass
    return translated_text


# get lyrics
def get_lyrics(self, path, dest):
    lyrics_text = ''
    if path.endswith('.lrc'):
        with open(path, "r", encoding='utf-8') as file:
            for line in file:
                line = line.replace('{space}', '').strip()
                try:
                    line_text = line.split(']')[1].strip()
                    if dest == '':
                        lyrics_text += f'{line_text}\n'
                    else:
                        lyrics_text += f'{line_text} - {translate_to_arabic(line_text, dest)}\n'
                except:
                    line_text = '\n'
                self.description_update_box.emit("جاري الترجمة انتظر قليلا...")
    else:
        with open(path, "r", encoding='utf-8') as file:
            data = json.load(file)
            for item in data["lyrics"]:
                try:
                    line_text = item.get('first_lang')
                    if dest == '':
                        lyrics_text += f'{line_text}\n'
                    else:
                        lyrics_text += f'{line_text} - {translate_to_arabic(line_text, dest)}\n'
                except:
                    line_text = '\n'
                self.description_update_box.emit("جاري الترجمة انتظر قليلا...")
    return lyrics_text


# get tags
def get_tags(song_name, artist_name):
    with open("functions/make_tags.txt", "r", encoding='utf-8') as tags_file:
        new_tags = (tags_file.read()).replace('{song_name}', song_name).replace('{artist_name}', artist_name)
    return new_tags


# generate description
def GenerateDescriptionNow(self, path, SongName, ArtistName, ArtistYtLink, ArtistSpotyLink, YourYtName, YourYtLink, YourTwLink, Translate, ArtistGender, YourFbLink, YourIgLink):
    if len(path) != 0:
        if Translate == "without translation":
            full_lyrics = get_lyrics(self, path, '')
        elif Translate.startswith('translate'):
            if Translate == "translate to arabic":
                translate_code = "ar"
            elif Translate == "translate to english":
                translate_code = "en"
            elif Translate == "translate to spanish":
                translate_code = "es"
                
            full_lyrics = get_lyrics(self, path, translate_code)
            
        # build title
        final_title = f"{SongName} مترجمه | Arabic subtitles - {ArtistName}"
            
        # female & male
        female = ['للفنانة', 'الفنانة', 'قنواتها']
        male = ['للفنان', 'الفنان', 'قنواته']
        group = ['للفرقة', 'الفرقة', 'قنواتهم']
        
        if ArtistGender == "artist is male":
            part_1, part_2, part_3 = male[0], male[1], male[2]
        elif ArtistGender == "artist is female":
            part_1, part_2, part_3 = female[0], female[1], female[2]
        elif ArtistGender == "artist is a group":
            part_1, part_2, part_3 = group[0], group[1], group[2]
        
        
        # build description
        final_description = f"""مرحبًا بكم في قناتنا! في هذا الفيديو، نقدم لكم أغنية '{SongName}' {part_1} {ArtistName} مع الترجمة العربية (مترجمة) لجميع محبي الموسيقى الناطقين بالعربية. انغمس في اللحن الساحر وكلمات الأغنية المؤثرة، مترجمة الآن لمتعتك. لا تنسى الإعجاب والمشاركة والاشتراك لمزيد من مقاطع الفيديو الموسيقية المترجمة!

🎵 الأغنية: {SongName}
🎤 {part_2}: {ArtistName}
🌙 الترجمة العربية: {YourYtName}

🔔 اشترك في قناتنا لمزيد من مقاطع الفيديو الموسيقية المترجمة: {YourYtLink}

📱 تواصل معنا عبر وسائل التواصل الاجتماعي:
- تويتر: {YourTwLink}
- فيسبوك: {YourFbLink}
- انستغرام: {YourIgLink}

🎧 للاستماع إلى المزيد من أغاني {ArtistName}، تفضل بزيارة {part_3} الرسمية:
- يوتيوب (Youtube): {ArtistYtLink}
- سبوتيفاي (Spotify): {ArtistSpotyLink}

📝 الكلمات:
{full_lyrics}


تنويه: نحن لا نملك حقوق هذه الأغنية. جميع الحقوق محفوظة لـ {ArtistName} وشركة الإنتاج الخاصة بها. هذا الفيديو هو لأغراض الترفيه والتعليم فقط.

لا تتردد في تخصيص هذا الوصف لتناسب أسلوب ونغمة قناتك. إذا كنت بحاجة إلى أي مساعدة إضافية، فقط اسألني!

#أغنية #أغنية_هادئة #{SongName}_مترجمه #{ArtistName} #اغنية_مترجمه #اغنية_جديده #اغاني_مترجمة #اغاني_بالعربية
"""

        made_tags = get_tags(SongName, ArtistName)
        self.description_update_box.emit(final_description), self.title_update_box.emit(final_title), self.tags_update_box.emit(made_tags)
    else:
        self.description_update_box.emit("lyrics path is missing")

        
        
        
        