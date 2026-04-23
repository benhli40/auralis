import sys
import json
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from config import APP_NAME, WINDOW_HEIGHT, WINDOW_WIDTH, APP_ICON_PATH, SETTINGS_PATH, DEFAULT_MUSIC_FOLDERS
from database import MusicDatabase
from player import AudioPlayer
from scanner import MusicScanner
from theme import get_stylesheet
from ui.main_window import MainWindow


class FuturePlayerApp:
    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName(APP_NAME)
        self.qt_app.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        self.qt_app.setStyleSheet(get_stylesheet())

        self.database = MusicDatabase()
        self.database.initialize()

        self.scanner = MusicScanner(self.database)
        self.scanned_count = 0
        self.settings = self.load_settings()

        self.player = AudioPlayer()

        self.main_window = MainWindow(
        database=self.database,
        scanner=self.scanner,
        player=self.player,
        app_controller=self,
        app_name=APP_NAME,
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT,
    )

    def load_settings(self) -> dict:
        if not Path(SETTINGS_PATH).exists():
            return {
                "music_folders": [str(path) for path in DEFAULT_MUSIC_FOLDERS]
            }

        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    data.setdefault("music_folders", [str(path) for path in DEFAULT_MUSIC_FOLDERS])
                    return data
        except Exception:
            pass

        return {
            "music_folders": [str(path) for path in DEFAULT_MUSIC_FOLDERS]
        }


    def save_settings(self) -> None:
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
                json.dump(self.settings, file, indent=2)
        except Exception as exc:
            print(f"Failed to save settings: {exc}")


    def add_music_folder(self, folder_path: str) -> None:
        folder_path = str(Path(folder_path))

        if folder_path not in self.settings["music_folders"]:
            self.settings["music_folders"].append(folder_path)
            self.save_settings()

    def initialize_library(self) -> None:
        music_folders = self.settings.get("music_folders", [])
        if not music_folders:
            self.scanned_count = 0
            print("No saved music folders found.")
            return

        self.scanned_count = self.scanner.scan(music_folders)
        print(f"Scanned {self.scanned_count} tracks from saved folders.")

    def run(self) -> int:
        self.initialize_library()
        self.main_window.show()
        return self.qt_app.exec()

    def shutdown(self) -> None:
        self.database.close()