import os
import json
from source.offline import offline

class MENUSKA():
    def __init__(self):
        self.settings_file = "user/settings.json"
        self.data = {
            "last_path": "/home/user/music",
            "api_key": ""
                    }
        self.load_settings()

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.data = json.load(f)

    def start_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("WELCOME TO O2")
        print("1 - play online")
        print("2 - play offline")
        answer = int(input())
        if answer == 1: 
            print(1)
            self.online_menu() 
        elif answer == 2:
            self.offline_menu()
            
    def online_menu(self, api = None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Api key: ", self.data['api_key'])
        print("1 - library")
        print("2 - search")
        print("3 - switch api key")
        print("0 - back to main menu")
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

    def offline_menu(self):
        os.system('clf' if os.name == 'nt' else 'clear')
        print("last folder: ", self.data['last_path'])
        print("1 - start in last folder")
        print("2 - select folder")
        print("0 - back to main menu")
        answer = int(input())
        if answer == 2:
            new = input("new folder: ")
            self.data['last_path'] = new 
            self.save_settings()
            self.offline_menu()
        elif answer == 1: 
            m = offline()
            m.scan()
            m.display()
        elif answer == 0:
            self.start_menu()
            
    def offline_play_menu(self, player):
        while True:
            os.system('clear')
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
