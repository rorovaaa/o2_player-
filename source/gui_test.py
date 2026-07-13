import sys
import os
import json
import vlc
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QSlider,
                             QFileDialog, QInputDialog, QMessageBox, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor
from mutagen.mp3 import MP3
from mutagen.flac import FLAC


class RetroPlayer(QMainWindow):
    THEMES = {
        "blue": {
            "window": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a69bd, stop:0.5 #0c2461, stop:1 #1e3799)",
            "central": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c6382, stop:1 #1e3799)",
            "screen": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0a3d62, stop:1 #1e3799)",
            "screen_border": "#4a69bd",
            "cover_bg": "#000000",
            "cover_border": "#4a69bd",
            "cover_text": "#ffd93d",
            "track": "#ffffff",
            "artist": "#ffd93d",
            "time": "#a8e6cf",
            "indicator": "#6bcf7f",
            "ctrl_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a69bd, stop:1 #1e3799)",
            "ctrl_btn_border": "#3c6382",
            "ctrl_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6a89cc, stop:1 #3c6382)",
            "play_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6bcf7f, stop:1 #3db86f)",
            "play_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7fdf8f, stop:1 #4dc87f)",
            "play_btn_pressed": "#3db86f",
            "menu_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a69bd, stop:1 #1e3799)",
            "menu_btn_border": "#3c6382",
            "menu_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6a89cc, stop:1 #3c6382)",
            "slider_groove": "#0a3d62",
            "slider_handle": "#ffd93d",
            "slider_sub": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6bcf7f, stop:1 #ffd93d)",
            "theme_btn": "#4a69bd",
            "theme_btn_border": "#3c6382",
        },
        "yellow": {
            "window": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f9ca24, stop:0.5 #f0932b, stop:1 #eb4d4b)",
            "central": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c5ce7, stop:1 #a29bfe)",
            "screen": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d3436, stop:1 #636e72)",
            "screen_border": "#f9ca24",
            "cover_bg": "#000000",
            "cover_border": "#f9ca24",
            "cover_text": "#ffffff",
            "track": "#ffffff",
            "artist": "#f9ca24",
            "time": "#dfe6e9",
            "indicator": "#00cec9",
            "ctrl_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c5ce7, stop:1 #a29bfe)",
            "ctrl_btn_border": "#5f27cd",
            "ctrl_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d6ef8, stop:1 #b3a8ff)",
            "play_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f9ca24, stop:1 #f0932b)",
            "play_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffda44, stop:1 #ffa33b)",
            "play_btn_pressed": "#e08520",
            "menu_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c5ce7, stop:1 #a29bfe)",
            "menu_btn_border": "#5f27cd",
            "menu_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d6ef8, stop:1 #b3a8ff)",
            "slider_groove": "#2d3436",
            "slider_handle": "#f9ca24",
            "slider_sub": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00cec9, stop:1 #f9ca24)",
            "theme_btn": "#f9ca24",
            "theme_btn_border": "#f0932b",
        },
        "white": {
            "window": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #dfe6e9, stop:0.5 #b2bec3, stop:1 #636e72)",
            "central": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #dfe6e9)",
            "screen": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d3436, stop:1 #636e72)",
            "screen_border": "#b2bec3",
            "cover_bg": "#000000",
            "cover_border": "#b2bec3",
            "cover_text": "#dfe6e9",
            "track": "#2d3436",
            "artist": "#636e72",
            "time": "#0984e3",
            "indicator": "#6c5ce7",
            "ctrl_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #636e72, stop:1 #2d3436)",
            "ctrl_btn_border": "#2d3436",
            "ctrl_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7f8c8d, stop:1 #636e72)",
            "play_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0984e3, stop:1 #74b9ff)",
            "play_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a94f3, stop:1 #84c9ff)",
            "play_btn_pressed": "#0769b3",
            "menu_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #636e72, stop:1 #2d3436)",
            "menu_btn_border": "#2d3436",
            "menu_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7f8c8d, stop:1 #636e72)",
            "slider_groove": "#2d3436",
            "slider_handle": "#0984e3",
            "slider_sub": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0984e3, stop:1 #74b9ff)",
            "theme_btn": "#636e72",
            "theme_btn_border": "#2d3436",
        },
        "black": {
            "window": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0a0a0a, stop:0.5 #1a1a1a, stop:1 #2d2d2d)",
            "central": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a1a, stop:1 #0a0a0a)",
            "screen": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:1 #1a1a1a)",
            "screen_border": "#404040",
            "cover_bg": "#000000",
            "cover_border": "#404040",
            "cover_text": "#808080",
            "track": "#ffffff",
            "artist": "#b0b0b0",
            "time": "#606060",
            "indicator": "#404040",
            "ctrl_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d2d2d, stop:1 #1a1a1a)",
            "ctrl_btn_border": "#404040",
            "ctrl_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #404040, stop:1 #2d2d2d)",
            "play_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #404040, stop:1 #2d2d2d)",
            "play_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #505050, stop:1 #404040)",
            "play_btn_pressed": "#1a1a1a",
            "menu_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d2d2d, stop:1 #1a1a1a)",
            "menu_btn_border": "#404040",
            "menu_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #404040, stop:1 #2d2d2d)",
            "slider_groove": "#1a1a1a",
            "slider_handle": "#808080",
            "slider_sub": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #404040, stop:1 #808080)",
            "theme_btn": "#404040",
            "theme_btn_border": "#2d2d2d",
        },
        "purple": {
            "window": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:0.5 #a29bfe, stop:1 #fd79a8)",
            "central": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2d1b69, stop:1 #6c5ce7)",
            "screen": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a0d3d, stop:1 #2d1b69)",
            "screen_border": "#6c5ce7",
            "cover_bg": "#000000",
            "cover_border": "#6c5ce7",
            "cover_text": "#fd79a8",
            "track": "#ffffff",
            "artist": "#a29bfe",
            "time": "#fd79a8",
            "indicator": "#00cec9",
            "ctrl_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c5ce7, stop:1 #2d1b69)",
            "ctrl_btn_border": "#a29bfe",
            "ctrl_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d6ef8, stop:1 #3d2b79)",
            "play_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fd79a8, stop:1 #e84393)",
            "play_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff89b8, stop:1 #f853a3)",
            "play_btn_pressed": "#d83383",
            "menu_btn": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c5ce7, stop:1 #2d1b69)",
            "menu_btn_border": "#a29bfe",
            "menu_btn_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7d6ef8, stop:1 #3d2b79)",
            "slider_groove": "#1a0d3d",
            "slider_handle": "#fd79a8",
            "slider_sub": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00cec9, stop:1 #fd79a8)",
            "theme_btn": "#6c5ce7",
            "theme_btn_border": "#a29bfe",
        },
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("O2 Player")
        self.setFixedSize(500, 850)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.instance = vlc.Instance('--no-video')
        self.player = self.instance.media_player_new()

        self.playlist = []
        self.current_index = 0
        self.settings_file = "user/settings.json"
        self.data = self.load_settings()
        self.current_theme = "blue"

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(400)

        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self.update_battery)
        self.battery_timer.start(30000)

        self.init_ui()
        self.apply_theme(self.current_theme)
        self.update_battery()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_path": "", "api_key": "", "albums": "", "last_selected_album": ""}

    def save_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_battery_info(self):
        try:
            if sys.platform.startswith('linux'):
                for bat in ['BAT0', 'BAT1', 'BATC']:
                    battery_path = f'/sys/class/power_supply/{bat}'
                    if os.path.exists(battery_path):
                        capacity_file = os.path.join(battery_path, 'capacity')
                        status_file = os.path.join(battery_path, 'status')
                        if os.path.exists(capacity_file):
                            with open(capacity_file, 'r') as f:
                                capacity = int(f.read().strip())
                            status = "Discharging"
                            if os.path.exists(status_file):
                                with open(status_file, 'r') as f:
                                    status = f.read().strip()
                            return capacity, "Charging" in status
            return 100, False
        except:
            return 100, False

    def update_battery(self):
        level, is_charging = self.get_battery_info()
        if is_charging:
            self.battery_label.setText(f" {level}%")
        else:
            self.battery_label.setText(f"{level}%")
        if level <= 20:
            self.battery_label.setStyleSheet("color:#ff6b6b; font:bold 12px Arial;")
        elif is_charging:
            self.battery_label.setStyleSheet("color:#ffd93d; font:bold 12px Arial;")
        else:
            self.battery_label.setStyleSheet("color:#6bcf7f; font:bold 12px Arial;")

    def init_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 180))
        central.setGraphicsEffect(shadow)

        main = QVBoxLayout(central)
        main.setSpacing(20)
        main.setContentsMargins(30, 30, 30, 30)

        top_bar = QHBoxLayout()
        self.btn_theme = QPushButton("●")
        self.btn_theme.setFixedSize(40, 40)
        self.btn_theme.setObjectName("theme_btn")
        self.btn_theme.clicked.connect(self.cycle_theme)
        theme_shadow = QGraphicsDropShadowEffect()
        theme_shadow.setBlurRadius(10)
        theme_shadow.setColor(QColor(0, 0, 0, 100))
        self.btn_theme.setGraphicsEffect(theme_shadow)
        top_bar.addWidget(self.btn_theme)

        brand = QLabel("O2")
        brand.setStyleSheet("color:#ffffff; font:bold 24px Arial; letter-spacing:4px;")
        top_bar.addWidget(brand)
        top_bar.addStretch()
        self.battery_label = QLabel("100%")
        self.battery_label.setStyleSheet("color:#6bcf7f; font:bold 12px Arial;")
        top_bar.addWidget(self.battery_label)
        main.addLayout(top_bar)

        self.screen = QWidget()
        self.screen.setObjectName("lcd_screen")
        screen_layout = QVBoxLayout(self.screen)
        screen_layout.setSpacing(12)
        screen_layout.setContentsMargins(20, 20, 20, 20)

        self.cover = QLabel()
        self.cover.setFixedSize(250, 250)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setObjectName("cover_label")
        self.cover.setText("♪ NO COVER ♪")
        screen_layout.addWidget(self.cover, alignment=Qt.AlignmentFlag.AlignCenter)

        separator = QLabel()
        separator.setFixedHeight(20)
        screen_layout.addWidget(separator)

        self.track_label = QLabel("NO TRACK")
        self.track_label.setObjectName("track_label")
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_label.setWordWrap(True)
        self.track_label.setFixedHeight(50)
        screen_layout.addWidget(self.track_label)

        self.artist_label = QLabel("—")
        self.artist_label.setObjectName("artist_label")
        self.artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artist_label.setFixedHeight(30)
        screen_layout.addWidget(self.artist_label)

        time_row = QHBoxLayout()
        self.time_now = QLabel("00:00")
        self.time_now.setObjectName("time_label")
        self.time_total = QLabel("00:00")
        self.time_total.setObjectName("time_label")
        time_row.addWidget(self.time_now)
        time_row.addStretch()
        time_row.addWidget(self.time_total)
        screen_layout.addLayout(time_row)

        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setRange(0, 1000)
        self.progress.setValue(0)
        self.progress.setObjectName("progress_slider")
        self.progress.sliderPressed.connect(lambda: self.timer.stop())
        self.progress.sliderReleased.connect(lambda: (self.seek(), self.timer.start(400)))
        screen_layout.addWidget(self.progress)

        indicators = QHBoxLayout()
        self.stereo_label = QLabel("◉ STEREO")
        self.stereo_label.setObjectName("indicator")
        self.status_label = QLabel("READY")
        self.status_label.setObjectName("indicator")
        indicators.addWidget(self.stereo_label)
        indicators.addStretch()
        indicators.addWidget(self.status_label)
        screen_layout.addLayout(indicators)

        main.addWidget(self.screen)

        ctrl = QHBoxLayout()
        ctrl.setSpacing(25)

        self.btn_prev = QPushButton("⏮")
        self.btn_prev.setFixedSize(70, 70)
        self.btn_prev.setObjectName("ctrl_btn")
        self.btn_prev.clicked.connect(self.prev_track)

        self.btn_play = QPushButton("▶")
        self.btn_play.setFixedSize(90, 90)
        self.btn_play.setObjectName("play_btn")
        self.btn_play.clicked.connect(self.toggle_play)

        self.btn_next = QPushButton("⏭")
        self.btn_next.setFixedSize(70, 70)
        self.btn_next.setObjectName("ctrl_btn")
        self.btn_next.clicked.connect(self.next_track)

        ctrl.addStretch()
        ctrl.addWidget(self.btn_prev)
        ctrl.addWidget(self.btn_play)
        ctrl.addWidget(self.btn_next)
        ctrl.addStretch()
        main.addLayout(ctrl)

        vol_row = QHBoxLayout()
        vol_lbl = QLabel("🔊 VOL")
        vol_lbl.setObjectName("vol_label")
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(70)
        self.volume.valueChanged.connect(self.set_volume)
        self.volume.setFixedWidth(250)
        self.volume.setObjectName("volume_slider")
        vol_row.addStretch()
        vol_row.addWidget(vol_lbl)
        vol_row.addWidget(self.volume)
        vol_row.addStretch()
        main.addLayout(vol_row)

        menu_row = QHBoxLayout()
        self.btn_folder = QPushButton("📁 FOLDER")
        self.btn_folder.setObjectName("menu_btn")
        self.btn_folder.clicked.connect(self.select_folder)

        self.btn_album = QPushButton("💿 ALBUMS")
        self.btn_album.setObjectName("menu_btn")
        self.btn_album.clicked.connect(self.select_album)

        self.btn_power = QPushButton("⏻")
        self.btn_power.setFixedSize(60, 60)
        self.btn_power.setObjectName("power_btn")
        self.btn_power.clicked.connect(self.close)
        power_shadow = QGraphicsDropShadowEffect()
        power_shadow.setBlurRadius(15)
        power_shadow.setColor(QColor(255, 107, 107, 180))
        self.btn_power.setGraphicsEffect(power_shadow)

        menu_row.addWidget(self.btn_folder)
        menu_row.addWidget(self.btn_album)
        menu_row.addStretch()
        menu_row.addWidget(self.btn_power)
        main.addLayout(menu_row)

        self.set_volume(70)

    def apply_theme(self, theme_name):
        if theme_name not in self.THEMES:
            theme_name = "blue"
        self.current_theme = theme_name
        t = self.THEMES[theme_name]

        self.setStyleSheet(f"""
            QMainWindow {{
                background: {t['window']};
            }}
            #centralWidget {{
                background: {t['central']};
                border-radius: 12px;
            }}
            #lcd_screen {{
                background: {t['screen']};
                border: 3px solid {t['screen_border']};
                border-radius: 10px;
            }}
            #cover_label {{
                background: {t['cover_bg']};
                border: 3px solid {t['cover_border']};
                border-radius: 8px;
                color: {t['cover_text']};
                font: bold 18px Arial;
            }}
            #track_label {{
                color: {t['track']};
                font: bold 20px Arial;
                background: transparent;
                padding: 5px;
            }}
            #artist_label {{
                color: {t['artist']};
                font: bold 15px Arial;
                background: transparent;
            }}
            #time_label {{
                color: {t['time']};
                font: bold 13px Arial;
                background: transparent;
            }}
            #indicator {{
                color: {t['indicator']};
                font: bold 11px Arial;
                background: transparent;
            }}
            #vol_label {{
                color: {t['time']};
                font: bold 11px Arial;
            }}
            QPushButton#ctrl_btn {{
                background: {t['ctrl_btn']};
                border: 2px solid {t['ctrl_btn_border']};
                border-radius: 10px;
                color: #ffffff;
                font: bold 22px Arial;
            }}
            QPushButton#ctrl_btn:hover {{
                background: {t['ctrl_btn_hover']};
            }}
            QPushButton#ctrl_btn:pressed {{
                background: {t['ctrl_btn_border']};
            }}
            QPushButton#play_btn {{
                background: {t['play_btn']};
                border: none;
                border-radius: 45px;
                color: #ffffff;
                font: bold 30px Arial;
            }}
            QPushButton#play_btn:hover {{
                background: {t['play_btn_hover']};
            }}
            QPushButton#play_btn:pressed {{
                background: {t['play_btn_pressed']};
            }}
            QPushButton#menu_btn {{
                background: {t['menu_btn']};
                border: 2px solid {t['menu_btn_border']};
                border-radius: 8px;
                color: #ffffff;
                font: bold 13px Arial;
                padding: 12px 18px;
            }}
            QPushButton#menu_btn:hover {{
                background: {t['menu_btn_hover']};
            }}
            QPushButton#power_btn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff6b6b, stop:1 #c0392b);
                border: 3px solid #a93226;
                border-radius: 30px;
                color: #ffffff;
                font: bold 26px Arial;
            }}
            QPushButton#power_btn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff7b7b, stop:1 #e74c3c);
                border: 3px solid #c0392b;
            }}
            QPushButton#power_btn:pressed {{
                background: #922b21;
                border: 3px inset #7b241c;
            }}
            QPushButton#theme_btn {{
                background: {t['theme_btn']};
                border: 3px solid {t['theme_btn_border']};
                border-radius: 20px;
                color: #ffffff;
                font: bold 16px Arial;
            }}
            QPushButton#theme_btn:hover {{
                opacity: 0.8;
            }}
            QPushButton#theme_btn:pressed {{
                opacity: 0.6;
            }}
            #progress_slider, #volume_slider {{
                background: transparent;
            }}
            QSlider::groove:horizontal {{
                background: {t['slider_groove']};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {t['slider_handle']};
                width: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {t['slider_sub']};
                border-radius: 4px;
            }}
        """)

    def cycle_theme(self):
        themes = list(self.THEMES.keys())
        current_idx = themes.index(self.current_theme)
        next_idx = (current_idx + 1) % len(themes)
        self.apply_theme(themes[next_idx])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select music folder")
        if folder:
            self.data['last_path'] = folder
            self.save_settings()
            self.scan_folder(folder)

    def select_album(self):
        albums_path = self.data.get('albums', '')
        if not albums_path or not os.path.exists(albums_path):
            albums_path = QFileDialog.getExistingDirectory(self, "Select albums folder")
            if albums_path:
                self.data['albums'] = albums_path
                self.save_settings()

        if albums_path and os.path.exists(albums_path):
            albums = sorted([d for d in os.listdir(albums_path)
                             if os.path.isdir(os.path.join(albums_path, d))])
            if not albums:
                QMessageBox.information(self, "Albums", "No albums found in folder.")
                return
            item, ok = QInputDialog.getItem(self, "Select Album",
                                            "Choose album:", albums, 0, False)
            if ok and item:
                album_path = os.path.join(albums_path, item)
                self.data['last_selected_album'] = album_path
                self.save_settings()
                self.scan_folder(album_path)

    def scan_folder(self, path):
        ex = ('.mp3', '.wav', '.flac')
        self.playlist = []
        if not os.path.exists(path):
            return
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.lower().endswith(ex):
                    self.playlist.append(os.path.join(root, f))
        if self.playlist:
            self.current_index = 0
            self.load_track(0)
            self.status_label.setText(f"{len(self.playlist)} TRACKS")
        else:
            self.status_label.setText("EMPTY")

    def load_track(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            path = self.playlist[index]
            media = self.instance.media_new(path)
            self.player.set_media(media)
            self.update_metadata(path)
            self.status_label.setText(f"{index+1}/{len(self.playlist)}")

    def decode_text(self, text):
        if text is None:
            return ""
        if isinstance(text, str):
            return text
        if isinstance(text, bytes):
            for encoding in ['utf-8', 'utf-16', 'cp1251', 'latin-1']:
                try:
                    return text.decode(encoding)
                except:
                    continue
            return text.decode('latin-1', errors='ignore')
        return str(text)

    def update_metadata(self, path):
        filename = os.path.basename(path)
        artist = "Unknown Artist"
        title = os.path.splitext(filename)[0]
        cover_data = None

        try:
            if path.lower().endswith('.mp3'):
                audio = MP3(path)
                if audio.tags:
                    for tag in audio.tags.values():
                        if hasattr(tag, 'FrameID'):
                            if tag.FrameID == 'TIT2' and tag.text:
                                title = self.decode_text(tag.text[0])
                            elif tag.FrameID == 'TPE1' and tag.text:
                                artist = self.decode_text(tag.text[0])
                            elif tag.FrameID == 'APIC':
                                cover_data = tag.data
            elif path.lower().endswith('.flac'):
                audio = FLAC(path)
                if 'title' in audio:
                    title = self.decode_text(audio['title'][0])
                if 'artist' in audio:
                    artist = self.decode_text(audio['artist'][0])
                if audio.pictures:
                    cover_data = audio.pictures[0].data
        except Exception as e:
            pass

        self.track_label.setText(title[:40])
        self.artist_label.setText(artist[:35])

        if cover_data:
            pixmap = QPixmap()
            pixmap.loadFromData(cover_data)
            if not pixmap.isNull():
                scaled = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                self.cover.setPixmap(scaled)
            else:
                self.cover.setText("♪ NO COVER ♪")
        else:
            self.cover.setText("♪ NO COVER ♪")

    def toggle_play(self):
        if self.player.is_playing():
            self.player.pause()
            self.btn_play.setText("▶")
            self.status_label.setText("PAUSED")
        else:
            if self.playlist:
                self.player.play()
                self.btn_play.setText("⏸")
                self.status_label.setText("PLAYING")

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_track(self.current_index)
            self.player.play()
            self.btn_play.setText("⏸")

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_track(self.current_index)
            self.player.play()
            self.btn_play.setText("⏸")

    def seek(self):
        if self.player.is_playing() or self.playlist:
            length = self.player.get_length()
            if length > 0:
                self.player.set_position(self.progress.value() / 1000.0)

    def set_volume(self, value):
        self.player.audio_set_volume(value)

    def update_progress(self):
        if self.playlist:
            length = self.player.get_length()
            position = self.player.get_time()
            if length > 0 and position >= 0:
                self.progress.blockSignals(True)
                self.progress.setValue(int(position / length * 1000))
                self.progress.blockSignals(False)
                self.time_now.setText(self.fmt(position))
                self.time_total.setText(self.fmt(length))
                if position >= length - 300:
                    self.next_track()

    def fmt(self, ms):
        s = int(ms / 1000)
        return f"{s//60:02d}:{s%60:02d}"

    def closeEvent(self, event):
        self.player.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    player = RetroPlayer()
    player.show()
    sys.exit(app.exec())