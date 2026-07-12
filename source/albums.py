import json
import os

class Albums:
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

    def select_folder_from_path(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        base_path = self.data.get("albums", "")
        
        if not base_path or not os.path.exists(base_path) or not os.path.isdir(base_path):
            print(f"Error: Path '{base_path}' not found or is not a directory.")
            input("Press Enter to return...")
            return None

        folders = []
        for item in os.listdir(base_path):
            full_path = os.path.join(base_path, item)
            if os.path.isdir(full_path):
                folders.append((item, full_path))

        if not folders:
            print(f"No folders found inside '{base_path}'.")
            input("Press Enter to return...")
            return None

        folder_dict = {}
        for index, (name, path) in enumerate(folders, start=1):
            folder_dict[index] = {"name": name, "path": path}

        print(f"\n--- Available albums in: {base_path} ---")
        for num, info in folder_dict.items():
            print(f"{num} - {info['name']}")
        print("0 - Cancel")

        while True:
            try:
                choice = int(input("\nSelect album number: "))
                if choice == 0:
                    print("Selection canceled.")
                    return None
                if choice in folder_dict:
                    selected_path = folder_dict[choice]["path"]
                    print(f"Selected: {folder_dict[choice]['name']}")
                    self.data['last_selected_album'] = selected_path
                    self.save_settings()
                    return selected_path
                else:
                    print("Invalid number, try again.")
            except ValueError:
                print("Please enter a number!")
