from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
CACHE_DIR = BASE_DIR / "cache"
DATABASE_PATH = BASE_DIR / "future_player.db"
SETTINGS_PATH = BASE_DIR / "settings.json"

APP_ICON_PATH = ASSETS_DIR / "app_icon.ico"

# App info
APP_NAME = "Auralis"
APP_VERSION = "0.1.0"

# Window defaults
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
MIN_WINDOW_WIDTH = 1100
MIN_WINDOW_HEIGHT = 700

# Supported audio formats
SUPPORTED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".ogg",
    ".flac",
    ".m4a",
}

# Default folders to scan
DEFAULT_MUSIC_FOLDERS = [
    Path.home() / "Music",
    Path(r"F:\My Music"),
]

# UI layout defaults
SIDEBAR_WIDTH = 220
RIGHT_PANEL_WIDTH = 320
BOTTOM_BAR_HEIGHT = 110

# Placeholder / cache settings
ALBUM_ART_SIZE = (280, 280)
THUMBNAIL_SIZE = (96, 96)

# Fallback metadata labels
UNKNOWN_ARTIST = "Unknown Artist"
UNKNOWN_ALBUM = "Unknown Album"
UNKNOWN_GENRE = "Unknown Genre"
UNKNOWN_TITLE = "Unknown Title"