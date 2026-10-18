from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QPushButton, QComboBox, QFileDialog, QApplication
from PyQt5.QtCore import QTime, QProcess, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys, os, requests
import pytube


# PAGES
MainPagePath = "ui/MainWindowV2.ui"
PreviewPagePath = "ui/FramePreview.ui"


# FUNCTIONS
from functions.GenerateDescription import *
from functions.GenerateVideo import *
from functions.GetYoutubeVideos import *
from functions.CollectGeniusAlbums import *


# MAIN        
class Main__(QMainWindow):
    def __init__(self):
        super(Main__, self).__init__()
        uic.loadUi(MainPagePath, self)
        
        # center app window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.showMaximized()
        

        # Add font to database
        font_path1 = QFontDatabase.addApplicationFont("assets/fonts/Lato/Lato-Regular.ttf")
        self.font_LatoRegular = QFontDatabase.applicationFontFamilies(font_path1)[0]

        font_path2 = QFontDatabase.addApplicationFont("assets/fonts/Lato/Lato-Bold.ttf")
        self.font_LatoBold = QFontDatabase.applicationFontFamilies(font_path2)[0]

        font_path3 = QFontDatabase.addApplicationFont("assets/fonts/Lato/Lato-Black.ttf")
        self.font_LatoBlack = QFontDatabase.applicationFontFamilies(font_path3)[0]


        # Set the custom font for all buttons
        font = QFont(self.font_LatoBold, weight=600, pointSize=9)
        buttons, combos = self.centralwidget.findChildren(QPushButton), self.centralwidget.findChildren(QComboBox)
        for button in buttons:
            button.setFont(font)
        for combo in combos:
            combo.setFont(font)


        # section 1
        self.CollectYoutubeVideoButton.clicked.connect(lambda: self.CollectYoutubeVideoThread())
        self.VideoFramePreview.clicked.connect(lambda: self.PreviewFrame())
        self.VideoBackgroundButton.clicked.connect(lambda: self.GetVideoBackgroundPath())
        self.VideoLogoButton.clicked.connect(lambda: self.GetVideoLogoPath())
        self.VideoSongButton.clicked.connect(lambda: self.GetVideoSongPath())
        self.VideoLyricsButton.clicked.connect(lambda: self.GetVideoLyricsPath())


        # section 2
        self.DescriptionLyricsButton.clicked.connect(lambda: self.GetLyricsPath())
        self.VideoBackground2Button.clicked.connect(lambda: self.GetVideoBackgroundPath())
        self.MakeYoutubeCover.clicked.connect(lambda: self.MakeYoutubeCoverNow())
        self.GenerateVideoDescriptionButton.clicked.connect(lambda: self.GenerateVideoDescription())


        # section 3
        self.table_add_lyrics.clicked.connect(lambda: self.add_lyrics_row())
        self.table_remove_lyrics.clicked.connect(lambda: self.delete_lyrics_row())
        self.load_data.clicked.connect(lambda: self.load_lyrics_data_to_table())
        self.translate_tableGO.clicked.connect(lambda: self.translate_table_google())
        self.translate_tableAI.clicked.connect(lambda: self.translate_table_AI())
        self.make_json_format.clicked.connect(lambda: self.save_table_lyrics_data())
        self.GenerateVideoButton.clicked.connect(lambda: self.run_command(self.EditorUpdates))


        # section 4
        self.CollectButton.clicked.connect(lambda: self.CollectInformationThread())
        self.SaveMetadata.clicked.connect(lambda: self.SaveMetadataToFolder())

        self.Lyrics_Combobox.currentIndexChanged.connect(self.lyricsCombo_changed)
        
        
        # generate description
        #self.DescriptionLyricsButton.clicked.connect(lambda: self.GetLyricsPath())
        

        # upload video
        #self.SelectVideoToUpload.clicked.connect(lambda: self.GetVideoFilePath())
        #self.UploadButton.clicked.connect(lambda: self.run_command_upload(self.upload_update_box))
        
        # add lyrics
        # 
        # 
        # 
        # self.make_json_format.clicked.connect(lambda: self.save_table_lyrics_data())
        # self.translate_table.clicked.connect(lambda: self.translate_table_google())
                
        # self.lyrics_table.setColumnWidth(0, 90)
        # self.lyrics_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        # cut Video
        # self.VideoPathButton.clicked.connect(lambda: self.GetVideoCutPath())
        # self.CutVideoButton.clicked.connect(lambda: self.CutVideoThread(self.CutVideoUpdateBox))
        # self.PlayPauseButton.clicked.connect(lambda: self.PlayPauseVideo())
        
        # self.MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.video_widget = QVideoWidget()
        # self.VideoGrind.addWidget(self.video_widget)
        
        # self.MediaPlayer.positionChanged.connect(self.update_video_slider)
        # self.VideoSlider.sliderMoved.connect(self.set_video_position)
        # self.MediaPlayer.durationChanged.connect(self.update_slider_range)
        # self.MediaPlayer.mediaStatusChanged.connect(self.handle_media_status)
        # self.MediaPlayer.positionChanged.connect(self.update_duration_label)
        
        # self.SetCutStart.clicked.connect(lambda: self.get_video_start_duration())
        # self.SetCutEnd.clicked.connect(lambda: self.get_video_end_duration())
        
        # self.CurrentVideoTime = 0
        
        # collect Information
        # self.CollectButton.clicked.connect(lambda: self.CollectInformationThread())
        # self.Lyrics_Combobox.currentIndexChanged.connect(self.lyricsCombo_changed)
        
        # self.AddToAlbumsButton.clicked.connect(lambda: self.GetYoutubeCover())
        # self.SaveMetadata.clicked.connect(lambda: self.SaveMetadataToFolder())
        
        # collect Youtube Video
        # self.CollectYoutubeVideoButton.clicked.connect(lambda: self.CollectYoutubeVideoThread())
        # self.SaveCollectYoutubeVideoButton.clicked.connect(lambda: self.GetSaveFolderCollectVideo())
        # self.ReSaveJson.clicked.connect(lambda: self.re_save_table_lyrics_data())
        #self.collectVideoMakeCover.clicked.connect(lambda: self.collectVideoMakeCoverFunction())

        self.show()
        

    # # collect video make cover
    # def collectVideoMakeCoverFunction(self):
    #     VideoBG = "C:/Users/Kada/Desktop/personal/personal/python programs/AutoEditor/gui/output/TestFolder/YoutubeCover.jpg"
    #     song_name_only = "Calm Down"
    #     second_word = "مترجمه للعربية"
    #     song_name_font_size = "230"
    #     second_word_font_size = "130"
    #     Transparnt = "5%"
    #     save_path = "C:/Users/Kada/Desktop/personal/personal/python programs/AutoEditor/gui/output/TestFolder/test_frame.png"

    #     make_cover = make_cover_now(self, VideoBG, song_name_only, second_word, song_name_font_size, second_word_font_size, save_path, Transparnt)
    #     FramePixmap = QPixmap(make_cover)
    #     self.ShowGeneratedCover.setScaledContents(True)
    #     self.ShowGeneratedCover.setPixmap(FramePixmap)

    # collect Youtube Video Function
    def CollectYoutubeVideoThread(self):
        save_folder = self.GetSaveFolderCollectVideo()
        self.CollectYoutubeVideoButton.setEnabled(False)
        if save_folder != "":
            self.VideoBox.setPlainText(f"[ DATA SAVE FOLDER ] - {save_folder}")
            self.collectYoutubeVideo_worker = ThreadCollectYoutubeVideoClass(self, save_folder)
            self.collectYoutubeVideo_worker.start()
            self.collectYoutubeVideo_worker.CollectVideoUpdate.connect(self.VideoBox.setPlainText)
            self.collectYoutubeVideo_worker.ChangeButtonName.connect(self.CollectYoutubeVideoButton.setText)

    # Get save folder
    def GetSaveFolderCollectVideo(self):
        save_folder_path = QFileDialog.getExistingDirectory(None, 'Select save folder', os.getenv('HOME'))
        return save_folder_path

    # re-save data
    def re_save_table_lyrics_data(self):
        lyrics_save_path = QFileDialog.getSaveFileName(self, 'Select lyrics json save file', os.getenv('HOME'), 'JSON(*.json)')[0]
        lyrics_table_data = {'lyrics': []}
        
        if lyrics_save_path != '':
            for row in range(self.VideoLyricsScraped.rowCount()):
                row_data = {}
                for column in range(self.VideoLyricsScraped.columnCount()):
                    item = self.VideoLyricsScraped.item(row, column)
                    if column == 0:
                        if item is not None:
                            row_data['show_time'] = item.text()
                        else:
                            row_data['show_time'] = item
                    elif column == 1:
                        if item is not None:
                            row_data['first_lang'] = item.text()
                        else:
                            row_data['first_lang'] = item
                    elif column == 2:
                        if item is not None:
                            row_data['second_lang'] = item.text()
                        else:
                            row_data['second_lang'] = item
                lyrics_table_data['lyrics'].append(row_data)
            
            with open(lyrics_save_path, "w", encoding='utf-8') as save_file:
                json.dump(lyrics_table_data, save_file, ensure_ascii=False)
        
    # save collected data
    def SaveMetadataToFolder(self):
        save_folder_path = QFileDialog.getExistingDirectory(None, 'Select save folder', os.getenv('HOME'))

        # get all data
        if save_folder_path != '':
            for i in range(self.FinalCollectInformation.rowCount()):
                song_name, song_logo, YouTube_cover, audio_url = self.FinalCollectInformation.item(i, 0), self.FinalCollectInformation.item(i, 1), self.FinalCollectInformation.item(i, 2), self.FinalCollectInformation.item(i, 3)
                lyrics = albums_lyrics.get(song_name.text())
                no_list = ['/', '\\', ':', '"', '*', '?', '<', '>', '|', '.']
                song_name_save = ""
                for letter in str(song_name.text()):
                    if letter not in no_list:
                        song_name_save += letter
 
                # make folder
                song_folder = f"{save_folder_path}/{song_name_save}"
                if not os.path.exists(song_folder):
                    os.makedirs(song_folder)
                                
                # add song lyrics - json
                json_lyrics = {"lyrics": []}
                for text in lyrics:
                    json_lyrics["lyrics"].append({"show_time": "00:00.00", "first_lang": lyrics.get(text), "second_lang": None})
                with open(f"{song_folder}/lyrics_json.json", "w", encoding='utf-8') as save_file:
                    json.dump(json_lyrics, save_file, ensure_ascii=False)
                
                # download logo
                if song_logo != None:
                    if song_logo.text() != '':
                        response = requests.get(song_logo.text())
                        if response.status_code == 200:
                            with open(f"{song_folder}/logo.png", 'wb') as file:
                                file.write(response.content)
                
                # download youtube cover
                if YouTube_cover != None:
                    if YouTube_cover.text() != '':
                        response = requests.get(YouTube_cover.text())
                        if response.status_code == 200:
                            with open(f"{song_folder}/Youtube_cover.jpg", 'wb') as file:
                                file.write(response.content)
                
                # download song audio
                if audio_url != None:
                    if audio_url.text() != '':
                        response = requests.get(audio_url.text())
                        if response.status_code == 200:
                            with open(f"{song_folder}/song.mp3", 'wb') as file:
                                file.write(response.content)
                
                
        
    # get youtube cover
    def GetYoutubeCover(self):
        yt = pytube.YouTube(self.AddToAlbums.text())
        thumbnail_url = yt.thumbnail_url
        
        try:
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            best_audio = audio_streams.first()
            song_url = best_audio.url
        except:
            session = requests.Session()
            get_links = session.post("https://yt1s.com/api/ajaxSearch/index", data={"q": self.AddToAlbums.text(), "vt": "mp3"})
            video_data = json.loads(get_links.text)
            audio_link, video_id = video_data.get("links").get("mp3").get("mp3128").get("k"), video_data.get("vid")
            convert = session.post("https://yt1s.com/api/ajaxConvert/convert", data={"vid": video_id, "k": audio_link})
            converted_video_data = json.loads(convert.text)
            song_url = converted_video_data.get("dlink")

        # Print the thumbnail URL
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(str(thumbnail_url)).content)
        self.YoutubeCover.setPixmap(pixmap)
        
        row_index = self.Lyrics_Combobox.currentIndex()
        if row_index != -1:
            self.FinalCollectInformation.setItem(row_index, 2, QTableWidgetItem(thumbnail_url))
            self.FinalCollectInformation.setItem(row_index, 3, QTableWidgetItem(song_url))

        
    # lyrics combobox
    def lyricsCombo_changed(self, index):
        global albums_lyrics

        self.LyricsTableSCraped.setRowCount(0)
        for idx, lyrics_data in enumerate(albums_lyrics.get(list(albums_lyrics.keys())[index])):
            lyrics_text = albums_lyrics.get(list(albums_lyrics.keys())[index]).get(lyrics_data)
            self.LyricsTableSCraped.setRowCount(idx+1), self.LyricsTableSCraped.setItem(idx, 0, QTableWidgetItem(str(lyrics_text)))
        
    # collect Information section
    def CollectInformationThread(self):
        global albums_lyrics
        
        GeniusURL = self.GeniusPath.text()
        if GeniusURL != '':
            albums_lyrics = {}
            albums_lyrics.clear()
            self.AlbumsTree.clear(), self.SaveMetadata.setEnabled(False), self.Lyrics_Combobox.setEnabled(False)

            self.collect_albums_worker = ThreadCollectGeniusAlbumsClass(self)
            self.collect_albums_worker.start()
            self.collect_albums_worker.genius_update_box.connect(self.CollectedBox.setPlainText)
            self.collect_albums_worker.album_logo_ready.connect(self.AlbumLogo.setPixmap)
            self.collect_albums_worker.album_name_ready.connect(self.AlbumTitle.setPlainText)
            self.collect_albums_worker.data_ready.connect(self.FillData)
        else:
            self.CollectedBox.setPlainText('No url was given')

    def FillData(self):
        global albums_lyrics, album_logo_url

        self.CollectedBox.setPlainText("writing albums information to tables")
        # lyrics combo box
        self.Lyrics_Combobox.clear(), self.FinalCollectInformation.setRowCount(0)
        for i in range(len(albums_lyrics)):
                self.Lyrics_Combobox.addItem(list(albums_lyrics.keys())[i])
                self.FinalCollectInformation.setRowCount(i+1), 
                self.FinalCollectInformation.setItem(i, 0, QTableWidgetItem(list(albums_lyrics.keys())[i]))
                self.FinalCollectInformation.setItem(i, 1, QTableWidgetItem(album_logo_url))
        
        # lyrics table
        self.LyricsTableSCraped.setRowCount(0)
        for idx, lyrics_data in enumerate(albums_lyrics.get(list(albums_lyrics.keys())[0])):
            lyrics_text = albums_lyrics.get(list(albums_lyrics.keys())[0]).get(lyrics_data)
            self.LyricsTableSCraped.setRowCount(idx+1), self.LyricsTableSCraped.setItem(idx, 0, QTableWidgetItem(str(lyrics_text)))

        self.CollectedBox.setPlainText("Done"), self.SaveMetadata.setEnabled(True), self.Lyrics_Combobox.setEnabled(True)

    def update_video_slider(self, position):
        self.VideoSlider.setValue(position)
    
    def set_video_position(self, position):
        self.MediaPlayer.setPosition(position)
    
    def update_slider_range(self, duration):
        self.VideoSlider.setMaximum(duration)
        
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.PlayPauseButton.setText('Play')
    
    def get_video_start_duration(self):
        self.StartCut.setText(str(self.CurrentVideoTime))
        
    def get_video_end_duration(self):
        self.EndCut.setText(str(self.CurrentVideoTime))
        
    def update_duration_label(self):
        duration = QTime(0, 0).addMSecs(self.MediaPlayer.position()).toString("hh:mm:ss")
        self.VideoCurrentDuration.setText(f"{duration}")
        self.CurrentVideoTime = duration
        
    # Generate Video
    def CutVideoThread(self, text_area):
        path, _ = QFileDialog.getSaveFileName(self, 'Save MP4 file', os.getenv('HOME'), 'MP4(*.mp4)')
        
        if path != '':
            self.CutVideoUpdateBox.setPlainText('starting soon...')
            
            # Create a process to run the command
            process = QProcess(self)
            process.setProcessChannelMode(QProcess.MergedChannels)
            process.readyRead.connect(lambda: self.CutVideoThread_handle_output(process, text_area))

            # Run the command
            VideoPath = self.VideoPathEdit.text()
            StartCut = self.StartCut.text()
            EndCut = self.EndCut.text()
            
            print (StartCut, EndCut)
            if StartCut != '' and EndCut != '':
                args = [VideoPath, StartCut, EndCut, path]
                
                process.start('python', ['pages/GenerateVideo.py', 'cut_video', *args])
                process.waitForFinished()
            else:
                self.CutVideoUpdateBox.setPlainText("Please select video start & end time to cut this video")

    def CutVideoThread_handle_output(self, process, text_area):
        # Read the output from the command and display it in the text area
        update_text = process.readAll().data().decode()
        text_area.clear()
        text_area.insertPlainText(update_text)
        
        
    def add_lyrics_row(self):
        table_count = self.lyrics_table.rowCount()
        self.lyrics_table.setRowCount(int(table_count)+1)
            
    def delete_lyrics_row(self):
        table_count = self.lyrics_table.rowCount()
        self.lyrics_table.setRowCount(int(table_count)-1)

    def translate_table_google(self):
        for row in range(self.lyrics_table.rowCount()):
            item = self.lyrics_table.item(row, 1)
            translated_text = translate_to_arabic(item.text(), 'ar')
            self.lyrics_table.setItem(row, 2, QTableWidgetItem(str(translated_text)))

    def translate_table_AI(self):
        for row in range(self.lyrics_table.rowCount()):
            item = self.lyrics_table.item(row, 1)
            while True:
                key, model = random.choice(open_ai_keys), random.choice(ai_models)
                ar_text = translate_to(item.text(), key, model)
                if ar_text != False:
                    break

            self.lyrics_table.setItem(row, 2, QTableWidgetItem(str(ar_text)))
        
    def load_lyrics_data_to_table(self):
        lyrics_path = QFileDialog.getOpenFileName(self, 'Select lyrics file', os.getenv('HOME'), 'LRC, JSON(*.lrc *.json)')[0]
        if lyrics_path != '':
            self.lyrics_table.setRowCount(0)
            
            if lyrics_path.endswith('.lrc'):
                with open(lyrics_path, 'r', encoding='utf-8') as lyrics_file:
                    for row_counter, line in enumerate(lyrics_file, start=1):
                        show_time, first_lang = line.strip().split(']')[0][1:], line.strip().split(']')[1]
                        self.lyrics_table.insertRow(row_counter-1)
                        self.lyrics_table.setItem(row_counter-1, 0, QTableWidgetItem(str(show_time)))
                        self.lyrics_table.setItem(row_counter-1, 1, QTableWidgetItem(str(first_lang)))
            elif lyrics_path.endswith('.json'):
                with open(lyrics_path, 'r', encoding='utf-8') as file:
                    lyrics_data = json.load(file)
                    for row_counter, line in enumerate(lyrics_data.get('lyrics'), start=1):
                        self.lyrics_table.insertRow(row_counter-1)
                        self.lyrics_table.setItem(row_counter-1, 0, QTableWidgetItem('' if line.get('show_time') is None else line.get('show_time')))
                        self.lyrics_table.setItem(row_counter-1, 1, QTableWidgetItem('' if line.get('first_lang') is None else line.get('first_lang')))
                        self.lyrics_table.setItem(row_counter-1, 2, QTableWidgetItem('' if line.get('second_lang') is None else line.get('second_lang')))

            
            
    def save_table_lyrics_data(self):
        lyrics_save_path = QFileDialog.getSaveFileName(self, 'Select lyrics json save file', os.getenv('HOME'), 'JSON(*.json)')[0]
        lyrics_table_data = {'lyrics': []}
        
        if lyrics_save_path != '':
            for row in range(self.lyrics_table.rowCount()):
                row_data = {}
                for column in range(self.lyrics_table.columnCount()):
                    item = self.lyrics_table.item(row, column)
                    if column == 0:
                        if item is not None:
                            row_data['show_time'] = item.text()
                        else:
                            row_data['show_time'] = item
                    elif column == 1:
                        if item is not None:
                            row_data['first_lang'] = item.text()
                        else:
                            row_data['first_lang'] = item
                    elif column == 2:
                        if item is not None:
                            row_data['second_lang'] = item.text()
                        else:
                            row_data['second_lang'] = item
                lyrics_table_data['lyrics'].append(row_data)
            
            with open(lyrics_save_path, "w", encoding='utf-8') as save_file:
                json.dump(lyrics_table_data, save_file, ensure_ascii=False)
        
    # Get video path
    def GetVideoFilePath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a video file', os.getenv('HOME'), 'MP4(*.mp4)')
        self.VideoUploadPath.setText(path[0])
        
    # Get video cut path 
    def GetVideoCutPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a cut video file', os.getenv('HOME'), 'MP4(*.mp4)')
        self.VideoPathEdit.setText(path[0])

        if path[0] != '':
            self.MediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path[0])))
            self.MediaPlayer.setVideoOutput(self.video_widget)
            self.SetCutStart.setEnabled(True), self.SetCutEnd.setEnabled(True), self.CutVideoButton.setEnabled(True)
            self.PlayPauseButton.setEnabled(True), self.MediaPlayer.play(), self.MediaPlayer.pause(), self.PlayPauseButton.setText('Play')
        
    # Play Pause Video
    def PlayPauseVideo(self):
        if self.MediaPlayer.state() == QMediaPlayer.PlayingState:
            self.MediaPlayer.pause()
            self.PlayPauseButton.setText('Play')
        else:
            self.MediaPlayer.play()
            self.PlayPauseButton.setText('Pause')
        
    # upload to youtube
    def run_command_upload(self, text_area_):
        self.upload_update_box.setText('uploading soon...')

        # Run the command
        VideoUploadPath = self.VideoUploadPath.text()
        VideoUploadTitle = self.VideoUploadTitle.text()
        VideoUploadDescription = self.VideoUploadDescription.toPlainText()
        VideoUploadCategory = self.VideoUploadCategory.currentText()
        VideoUploadKeywords = self.VideoUploadKeywords.toPlainText()
        VideoUploadStatus = self.VideoUploadStatus.currentText()
        
        #upload_video(VideoUploadPath, VideoUploadTitle, VideoUploadDescription, VideoUploadCategory, VideoUploadKeywords, VideoUploadStatus, self)

    def handle_output_upload(self, process_upload, text_area_):
        # Read the output from the command and display it in the text area
        update_text = process_upload.readAll().data().decode()
        text_area_.clear()
        text_area_.insertPlainText(update_text)
        
        
    # Generate Video
    def run_command(self, text_area):
        path, _ = QFileDialog.getSaveFileName(self, 'Save MP4 file', os.getenv('HOME'), 'MP4(*.mp4)')
        
        if path != "":
            self.GenerateVideoButton.setEnabled(False), self.GenerateVideoButton.setText("Editing ongoing...")

            # Create a process to run the command
            process = QProcess(self)
            process.setProcessChannelMode(QProcess.MergedChannels)
            process.readyRead.connect(lambda: self.handle_output(process, text_area))

            # Run the command
            VideoBG = self.VideoBackgroundPath.text()
            VideoLogo = self.VideoLogoPath.text()
            VideoSong = self.VideoSongPath.text()
            VideoLyrics = self.VideoLyricsPath.text()
            VideoSongTitle = self.VideoSongTitle.text()
            VideoSongAlbum = self.VideoSongAlbum.text()
            VideoTranslate = self.VideoLyricsType.currentText()
            VideoQuality = self.VideoQualty.currentText()
            VideoLength = self.VideoLength.currentText()
            VideoFontType = self.VideoFontType.currentText()
            Transparant = self.Transparant.currentText()
            
            if VideoLyrics.endswith('.json'):
                lyrics_type = "json_type"
            if VideoLyrics.endswith('.lrc'):
                lyrics_type = "lrc_type"

            self.EditorUpdates.setPlainText('Editing will start soon...')
            if VideoBG != '' and VideoLogo != '' and VideoSong != '' and VideoLyrics != '' and VideoSongTitle != '' and VideoSongAlbum != '':
                args = [VideoBG, VideoLogo, VideoSong, VideoLyrics, VideoSongTitle, VideoSongAlbum, VideoTranslate, VideoQuality, VideoLength, VideoFontType, path, lyrics_type, Transparant]
                process.start('python', ['functions/GenerateVideo.py', 'generate_video', *args])
                process.waitForFinished()
            else:
                self.EditorUpdates.setPlainText('background, logo, song audio, lyrics, song title and song album are required.')
            self.GenerateVideoButton.setEnabled(True), self.GenerateVideoButton.setText("Make Video")

    def handle_output(self, process, text_area):
        # Read the output from the command and display it in the text area
        update_text = process.readAll().data().decode()
        text_area.clear()
        text_area.insertPlainText(update_text)
    
    # Get Lyrics Path
    def GetLyricsPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a lyrics file', os.getenv('HOME'), 'LRC, JSON(*.lrc *json)')
        self.DescriptionLyricsPath.setText(path[0])
    
    # Get Lyrics Path
    def GetVideoBackgroundPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a background file', os.getenv('HOME'), 'PNG, JPG, JPEG(*.png *jpg *jpeg)')
        self.VideoBackgroundPath.setText(path[0]), self.VideoBackgroundPath2.setText(path[0])
    
    # Get Lyrics Path
    def GetVideoLogoPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a Logo file', os.getenv('HOME'), 'PNG, JPG, JPEG(*.png *jpg *jpeg)')
        self.VideoLogoPath.setText(path[0])
    
    # Get Lyrics Path
    def GetVideoSongPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a lyrics file', os.getenv('HOME'), 'MP3(*.mp3)')
        self.VideoSongPath.setText(path[0])
    
    # Get Lyrics Path
    def GetVideoLyricsPath(self):
        path = QFileDialog.getOpenFileName(self, 'Select a lyrics file', os.getenv('HOME'), 'LRC, JSON(*.lrc *.json)')
        self.VideoLyricsPath.setText(path[0])
    
    
    # Generate Video Description Function
    def GenerateVideoDescription(self):
        self.generate_description_worker = ThreadGenerateDescriptionClass(self)
        self.generate_description_worker.start()
        self.generate_description_worker.title_update_box.connect(self.Titlebox.setText)
        #self.generate_description_worker.title_update_box.connect(self.VideoUploadTitle.setText)
        self.generate_description_worker.tags_update_box.connect(self.Tagsbox.setPlainText)
        #self.generate_description_worker.tags_update_box.connect(self.VideoUploadKeywords.setText)
        self.generate_description_worker.description_update_box.connect(self.DescriptionBox.setPlainText)
        #self.generate_description_worker.description_update_box.connect(self.VideoUploadDescription.setText)
        
    # Preview Frame
    def PreviewFrame(self):
        VideoBG = self.VideoBackgroundPath.text()
        VideoLogo = self.VideoLogoPath.text()
        VideoSongTitle = self.VideoSongTitle.text()
        VideoSongAlbum = self.VideoSongAlbum.text()
        
        if VideoBG != '' and VideoLogo != '' and VideoSongTitle != '' and VideoSongAlbum != '':
            self.generate_video_worker = ThreadGenerateFrameClass(self)
            self.generate_video_worker.start()
            self.generate_video_worker.video_update_box.connect(self.VideoBox.setPlainText)
            self.generate_video_worker.frame_ready.connect(self.Show_Frame)
        else:
            self.VideoBox.setPlainText('background, logo, song title and song album are required.')
    
    # show frame    
    def Show_Frame(self):
        FramePixmap = QPixmap("assets/frame.png")
        self.CoverViewer.setScaledContents(True)
        self.CoverViewer.setPixmap(FramePixmap)

    # show frame    
    def Show_Frame2(self):
        FramePixmap = QPixmap("assets/frame.png")
        self.CoverViewer2.setScaledContents(True)
        self.CoverViewer2.setPixmap(FramePixmap)
    
    # make cover
    def MakeYoutubeCoverNow(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save Youtube Cover file', os.getenv('HOME'), 'PNG(*.png)')
        
        if path != '':
            VideoBG = self.VideoBackgroundPath2.text()
            song_name_only = self.song_name_only.text()
            second_word = self.cover_botton_word.text()
            
            if VideoBG != '' and song_name_only != '' and second_word != '':
                self.make_cover_worker = ThreadMakeCoverClass(self, path)
                self.make_cover_worker.start()
                self.make_cover_worker.video_update_box.connect(self.CoverBox.setPlainText)
                self.make_cover_worker.frame_ready.connect(self.Show_Frame2)
            else:
                self.CoverBox.setPlainText('background, song name and second word are required.')
        
    
# FRAME PREVIEW CLASS        
class FramePreview(QMainWindow):
    def __init__(self):
        super(FramePreview, self).__init__()
        uic.loadUi(PreviewPagePath, self)
        
        # center app window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# COLLECT GENIUS ALBUMS THREAD
class ThreadCollectGeniusAlbumsClass(QThread):    
    genius_update_box = pyqtSignal(str)
    album_logo_ready = pyqtSignal(QPixmap)
    album_name_ready = pyqtSignal(str)
    data_ready = pyqtSignal()

    def __init__(self, BeforeSelf, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.BeforeSelf = BeforeSelf

    def run(self):
        global albums_lyrics, album_logo_url

        GeniusURL = self.BeforeSelf.GeniusPath.text()
        albums_lyrics, album_logo_url = CollectAlbumsInformation(self, self.BeforeSelf, GeniusURL)
        self.data_ready.emit()
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()


# GENERATE VIDEO THREAD
class ThreadCollectYoutubeVideoClass(QThread):    
    CollectVideoUpdate = pyqtSignal(str)
    ChangeButtonName = pyqtSignal(str)

    def __init__(self, BeforeSelf, folder_path, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.BeforeSelf = BeforeSelf
        self.folder_path = folder_path

    def run(self):
        url, transcript_type = self.BeforeSelf.YoutubeVideoURL.text(), self.BeforeSelf.TranscriptType.currentText()
        if url != "":
            self.CollectVideoUpdate.emit('Starting soon...')
            url = url.split('watch?v=')[1].split('&')[0]
            try:
                GetVideo(self, self.BeforeSelf, url, self.folder_path, transcript_type)
            except Exception as error:
                self.CollectVideoUpdate.emit(f'[ ERROR ] - {error}')
        else:
            self.CollectVideoUpdate.emit('Please select youtube video url and the save folder')

        self.BeforeSelf.CollectYoutubeVideoButton.setEnabled(True)
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()


# GENERATE DESCRIPTION THREAD
class ThreadGenerateDescriptionClass(QThread):
    description_update_box = pyqtSignal(str)
    title_update_box = pyqtSignal(str)
    tags_update_box = pyqtSignal(str)

    def __init__(self, BeforeSelf, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.BeforeSelf = BeforeSelf

    def run(self):
        LyricsPath = self.BeforeSelf.DescriptionLyricsPath.text()
        SongName_Keyword = self.BeforeSelf.SongName_Keyword.text()
        ArtistName = self.BeforeSelf.ArtistName.text()
        ArtistYtLink = self.BeforeSelf.ArtistYoutubeChannelLink.text()
        ArtistSpotyLink = self.BeforeSelf.ArtistSpofityLink.text()
        YourYtName = self.BeforeSelf.YourYoutubeChannelName.text()
        YourYtLink = self.BeforeSelf.YourYoutubeChannelLink.text()
        YourTwLink = self.BeforeSelf.YourTwitterLink.text()
        Translate = self.BeforeSelf.DescriptionLyricsType.currentText()
        ArtistGender = self.BeforeSelf.ArtistGender.currentText()
        YourFbLink = self.BeforeSelf.YourFacebookLink.text()
        YourIgLink = self.BeforeSelf.YourInstagramLink.text()
        
        GenerateDescriptionNow(self, LyricsPath, SongName_Keyword, ArtistName, ArtistYtLink, ArtistSpotyLink, YourYtName, YourYtLink, YourTwLink, Translate, ArtistGender, YourFbLink, YourIgLink)
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
        
# GENERATE VIDEO THREAD
class ThreadGenerateFrameClass(QThread):    
    video_update_box = pyqtSignal(str)
    frame_ready = pyqtSignal()

    def __init__(self, BeforeSelf, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.BeforeSelf = BeforeSelf

    def run(self):
        VideoBG = self.BeforeSelf.VideoBackgroundPath.text()
        VideoLogo = self.BeforeSelf.VideoLogoPath.text()
        VideoSongTitle = self.BeforeSelf.VideoSongTitle.text()
        VideoSongAlbum = self.BeforeSelf.VideoSongAlbum.text()
        Transparnt = self.BeforeSelf.Transparant.currentText()
        
        generate_frame = generate_frame_1080p(self, VideoBG, VideoLogo, VideoSongTitle, VideoSongAlbum, Transparnt)
        self.frame_ready.emit()
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
        

# GENERATE VIDEO THREAD
class ThreadMakeCoverClass(QThread):    
    video_update_box = pyqtSignal(str)
    frame_ready = pyqtSignal()

    def __init__(self, BeforeSelf, path, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.BeforeSelf = BeforeSelf
        self.save_path = path

    def run(self):
        VideoBG = self.BeforeSelf.VideoBackgroundPath2.text()
        song_name_only = self.BeforeSelf.song_name_only.text()
        song_name_font_size = self.BeforeSelf.song_name_font_size.currentText()
        second_word_font_size = self.BeforeSelf.second_word_font_size.currentText()
        second_word = self.BeforeSelf.cover_botton_word.text()
        Transparnt = self.BeforeSelf.Transparant2.currentText()
        
        make_cover = make_cover_now(self, VideoBG, song_name_only, second_word, song_name_font_size, second_word_font_size, self.save_path, Transparnt)
        self.frame_ready.emit()
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()


        

# RUN FOREVER
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main__()
    try:
        sys.exit(app.exec_())
    except:
        print ("user left")