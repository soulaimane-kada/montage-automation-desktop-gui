from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QPixmap

from bs4 import BeautifulSoup
import requests



def CollectAlbumsInformation(self, thread_self, GeniusURL):
    albums_lyrics = {}

    try:
        self.genius_update_box.emit("Connecting to genius...")

        soup = BeautifulSoup(requests.get(GeniusURL).content, "html.parser")
        albums = [album for album in soup.select(".chart_row-content")]
        
        # album info
        logo_url = soup.find("img", class_="cover_art-image").get("src")
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(logo_url).content)
        self.album_logo_ready.emit(pixmap)
        self.album_name_ready.emit(soup.find("h1", class_="header_with_cover_art-primary_info-title").text), 
        
        self.genius_update_box.emit("getting albums information..")
        # albums
        for idx, album in enumerate(albums, start=1):
            song_title, lyrics_url = album.find("h3", class_="chart_row-content-title").contents[0].strip(), album.find("a", class_="u-display_block").get("href")
            child_item = QTreeWidgetItem(thread_self.AlbumsTree, [str(song_title)])
            grandchild_item = QTreeWidgetItem(child_item, [str(lyrics_url)])
            
            # get lyrics
            lyrics_soup = BeautifulSoup(requests.get(str(lyrics_url)).content, "html.parser")
            lyrics_elements = lyrics_soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-1")
            
            albums_lyrics[f"{song_title}"], counter = {}, 1
            for lyrics_part in lyrics_elements:
                new_soup = BeautifulSoup(str(lyrics_part).replace("<br/>", "\n"), "html.parser")
                
                for soup in new_soup:
                    for text in (soup.text).split("\n"):
                        if text.strip() != '' and not text.strip().startswith('['):
                            albums_lyrics[f"{song_title}"][f"text_{counter}"] = text.strip()
                            counter += 1

        return [albums_lyrics, logo_url]
    except Exception as error:
        self.genius_update_box.emit(f'Something wrong happened.\n\n[ERROR] -->> {error}')


