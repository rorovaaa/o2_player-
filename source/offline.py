import time
import json
import os
import vlc

class offline:
    def __init__(self, path_f=None):
        from user.menu import MENUSKA
        self.menu = MENUSKA()
        
        if path_f:
            self.path = path_f
        else:
            try:
                with open('user/settings.json', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    self.path = data.get('last_path', '')
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
        
        if not os.path.exists(self.path):
            print(f"Folder {self.path} not found!")
            return

        for root, dirs, files in os.walk(self.path):
            songs = [f for f in files if f.lower().endswith(ex)]
            if songs:
                folder_name = os.path.basename(root) or root
                self.library[folder_name] = songs
                for s in songs:
                    self.playlist.append(os.path.join(root, s))

    def display(self):
        if not self.library:
            print("No music found.")
            input("Press Enter...")
            self.menu.offline_menu()
            return
        
        self.menu.offline_play_menu(self)

    def play(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            media = self.instance.media_new(self.playlist[self.current_index])
            self.player.set_media(media)
            self.player.play()
            print(f"▶ Playing: {os.path.basename(self.playlist[self.current_index])}")

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play(self.current_index)

    def prev(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play(self.current_index)

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()
