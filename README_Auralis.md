# Auralis

Auralis is a modern desktop music player and library manager built with **Python** and **PySide6**.

It was designed to feel cleaner, sleeker, and more future-facing than a traditional media player while still giving you control over your own local music library. Auralis scans your music folders, builds a local database, lets you browse by **Artists**, **Albums**, **Genres**, and **Songs**, and plays tracks through a custom desktop interface with a dedicated now-playing panel and transport controls.

## Highlights

- Modern desktop UI built with **PySide6**
- Local library scanning and metadata indexing
- Browse music by:
  - Artists
  - Albums
  - Genres
  - Songs
- Now Playing panel with album art support
- Playback controls:
  - Play
  - Pause
  - Previous
  - Next
  - Shuffle
  - Repeat
  - Seek
  - Volume
- Metadata editing tools inside the app
  - Rename artists
  - Rename genres
- Saved music folder support
- Local SQLite database for fast library access
- Custom theming for a sleek, dark, modern look

## Project Status

Auralis is an active work-in-progress and is already functional as a local desktop music player. The current version focuses on core library management, playback, and UI structure. Future versions will continue improving polish, metadata editing, queue behavior, and library experience.

## Tech Stack

- **Python**
- **PySide6** for the desktop UI
- **SQLite** for local library storage
- **Mutagen** for audio metadata reading and writing
- **PyInstaller** for building a Windows executable

## Project Structure

```text
Auralis/
├── main.py
├── app.py
├── config.py
├── database.py
├── scanner.py
├── player.py
├── theme.py
├── models.py
├── assets/
├── cache/
└── ui/
    ├── __init__.py
    ├── main_window.py
    ├── library_view.py
    ├── now_playing.py
    ├── sidebar.py
    └── controls.py
```

## How Auralis Works

Auralis is built around four major layers:

### 1. Library Scanning
The scanner walks through your configured music folders, finds supported audio files, reads metadata, and adds the results to the local library database.

### 2. Database
A local SQLite database stores:
- artists
- albums
- genres
- tracks

This allows the app to load your library quickly without rebuilding everything from scratch every time.

### 3. Playback Engine
The playback layer handles track loading, play/pause, seek, position updates, duration updates, and transport controls.

### 4. UI Layer
The interface is divided into:
- **Sidebar** for navigation
- **Main View** for library browsing
- **Now Playing Panel** for artwork and queue
- **Controls Bar** for transport and playback controls

## Features

### Library
- Scan one or more music folders
- Build a local music database
- View artists, albums, genres, and songs
- Drill down into artist, album, and genre views

### Playback
- Double-click a song to play it
- Play/pause playback
- Seek within a track
- Volume control
- Next/previous track support
- Shuffle mode
- Repeat mode

### Metadata Editing
- Rename artists from within the app
- Rename genres from within the app
- Write metadata updates back to supported file tags

### Visual Design
- Dark modern theme
- Rounded panels
- Clean transport controls
- Dedicated album-art panel
- Structured layout designed for growth

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/auralis.git
cd auralis
```

### 2. Create and activate a virtual environment

#### Windows PowerShell
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Command Prompt
```cmd
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you do not yet have a `requirements.txt`, install the core dependencies manually:

```bash
pip install PySide6 mutagen pillow pyinstaller
```

## Running Auralis

```bash
python main.py
```

## Building a Windows Executable

To package Auralis as a Windows `.exe` with PyInstaller:

```powershell
pyinstaller --windowed --noconsole --name Auralis --icon assets\app_icon.ico --add-data "assets;assets" main.py
```

The built executable will usually be created here:

```text
dist\Auralis\Auralis.exe
```

For a clean rebuild, delete:
- `build/`
- `dist/`
- `Auralis.spec`

and run the command again.

## Configuration

Auralis uses `config.py` for core defaults such as:
- application name
- window size
- asset paths
- cache paths
- database location
- default music folders

Auralis can also remember music folders through a local settings file so you do not have to keep selecting the same library path every time.

## Supported Library Behavior

Auralis is intended to support local music folders such as:

```python
DEFAULT_MUSIC_FOLDERS = [
    Path.home() / "Music",
    Path(r"F:\My Music"),
]
```

You can also add folders through the UI using **Scan Folder**.

## Roadmap

Planned and in-progress ideas include:

- Better queue management
- Improved shuffle history behavior
- Repeat-one vs repeat-library modes
- Richer album art handling
- Folder memory and smarter startup scanning
- More metadata editing tools
- Album rename support
- Better artist merge/cleanup tools
- Playlist creation and editing
- Search and filtering
- Visual polish and icon improvements
- Improved packaging and release workflow

## Why Auralis?

Auralis is meant to be more than a basic player. The goal is to build a music app that feels:
- modern
- personal
- local-first
- visually polished
- more premium than the average default media player

It is designed for people who want ownership over their music library and a cleaner listening experience on desktop.

## Known Issues / Work in Progress

Because Auralis is under active development, some areas may still be rough around the edges:

- some metadata editing workflows may need refinement
- startup scanning behavior may continue to evolve
- artwork support depends on embedded tags or available cover images
- shuffle/repeat behavior may continue to improve
- some library-management tools are still being built out

## Contributing

Contributions, ideas, cleanup suggestions, and UI polish feedback are welcome.

If you would like to improve Auralis:
1. fork the repo
2. create a feature branch
3. make your changes
4. open a pull request

## License

Choose a license before publishing publicly.

A common starting point is the **MIT License** if you want something simple and permissive.

## Author

Built by **Benjamin Liles**.

## Notes

Auralis is a personal music-player project focused on modern local-library playback, metadata management, and a cleaner desktop listening experience.

If you are building your own version or learning from the project, the best place to start is:
- `app.py`
- `database.py`
- `scanner.py`
- `ui/main_window.py`
