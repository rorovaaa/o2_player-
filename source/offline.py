import time 
import json
import os
import vlc 

class offline():
    def __init__(self):
        from user.menu import MENUSKA
        self.menu = MENUSKA()
        try:
            with open('user/settings.json', 'r') as f:
                self.data = json.load(f)
                self.path = self.data.get('last_path', '')
        except:
            self.path = ""

        self.library = {}
        self.playlist = [] 
        self.current_index = 0
        self.instance = vlc.Instance('--no-video') 
        self.player = self.instance.media_player_new()

    def scan(self):
        ex = ('.mp3', '.wav', '.flac')
        self.library = {}
        self.playlist = [] 
        
        for root, dirs, files in os.walk(self.path):
            songs = [f for f in files if f.lower().endswith(ex)]
            if songs:
                folder_name = os.path.basename(root) or root
                self.library[folder_name] = songs
                for s in songs:
                    self.playlist.append(os.path.join(root, s))

    def display(self):
        if not self.library:
            self.menu.offline_menu()
            return
        
        global_index = 1
        for folder, songs in self.library.items():
            print(f"Folder: {folder}")
            for song in songs:
                print(f"  {global_index}. {song}")
                global_index += 1
        self.menu.offline_play_menu(self)
    def play(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            media = self.instance.media_new(self.playlist[self.current_index])
            self.player.set_media(media)
            self.player.play()
            print(f"▶ Playing: {os.path.basename(self.playlist[self.current_index])}")

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play(self.current_index)

    def prev(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play(self.current_index)

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()
