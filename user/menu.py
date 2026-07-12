import os
import json
import sys

from source.offline import offline
from source.albums import Albums

class MENUSKA:
    def __init__(self):
        self.settings_file = "user/settings.json"
        self.data = {
            "last_path": "/home/user/music",
            "api_key": "",
            "albums": "",
            "last_selected_album": ""
        }
        self.load_settings()

    def save_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def start_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("WELCOME TO O2")
        print("1 - play online")
        print("2 - play offline")
        try:
            answer = int(input("Select option: "))
            if answer == 1: 
                self.online_menu() 
            elif answer == 2:
                self.offline_menu()
            else:
                self.start_menu()
        except ValueError:
            self.start_menu()

    def online_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Api key: ", self.data.get('api_key', ''))
        print("1 - library")
        print("2 - search")
        print("3 - switch api key")
        print("0 - back to main menu")
        try:
            answer = int(input())
            if answer == 1:
                print("test_library")
            elif answer == 2:
                print("test_search")
            elif answer == 0:
                self.start_menu()
            elif answer == 3:
                new = input("new api key: ")
                self.data['api_key'] = new 
                self.save_settings()
                self.online_menu()
        except ValueError:
            self.online_menu()

    def offline_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("last folder: ", self.data.get('last_path', ''))
        print("1 - start in last folder")
        print("2 - select folder")
        print("3 - albums")
        print("0 - back to main menu")
        try:
            answer = int(input())
            if answer == 2:
                new = input("new folder: ")
                self.data['last_path'] = new 
                self.save_settings()
                self.offline_menu()
            elif answer == 1: 
                m = offline(path_f=self.data.get('last_path', ''))
                m.scan()
                m.display()
            elif answer == 3:
                self.albums_path()
            elif answer == 0:
                self.start_menu()
        except ValueError:
            self.offline_menu()

    def offline_play_menu(self, player):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== SONGS ===")
            for i, song_path in enumerate(player.playlist):
                marker = " > " if i == player.current_index else "   "
                print(f"{marker}{i+1}. {os.path.basename(song_path)}")
            
            print("\n=== CONTROL MENU ===")
            print("1 - play choice")
            print("2 - next")
            print("3 - prev")
            print("4 - pause")
            print("5 - stop")
            print("0 - main menu")
            try:
                answer = int(input())
            except ValueError:
                continue
            
            if answer == 1:
                try:
                    choice = int(input("Enter song number: ")) - 1
                    player.play(choice)
                except:
                    print("Invalid number")
            elif answer == 2:
                player.next()
            elif answer == 3:
                player.prev()
            elif answer == 4:
                player.pause()
            elif answer == 5:
                player.stop()
            elif answer == 0:
                player.stop()
                self.start_menu()
                return

    def albums_path(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        a = Albums()
        print("=== ALBUMS ===")
        print("Current albums folder:", self.data.get('albums', 'Not set'))
        print("1 - select album")
        print("2 - set albums folder")
        print("0 - main menu")
        
        try:
            ans = int(input())
        except ValueError:
            self.albums_path()
            return

        match ans:
            case 1:
                selected = a.select_folder_from_path()
                if selected:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    m = offline(path_f=selected)
                    m.scan()
                    m.display()
                else:
                    self.albums_path()
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                new = input("Enter albums folder path: ")
                self.data['albums'] = new 
                self.save_settings()
                self.albums_path()
            case 0:
                self.start_menu()
            case _:
                self.albums_path()

