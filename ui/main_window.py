import random

from pathlib import Path
from mutagen import File as MutagenFile
from config import APP_ICON_PATH, CACHE_DIR

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QMainWindow, QSplitter, QVBoxLayout, QWidget

from config import APP_ICON_PATH
from ui.controls import ControlsPanel
from ui.library_view import LibraryView
from ui.now_playing import NowPlayingPanel
from ui.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(
        self,
        database,
        scanner,
        player,
        app_controller,
        app_name: str,
        window_width: int,
        window_height: int,
    ) -> None:
        
        super().__init__()

        self.database = database
        self.scanner = scanner
        self.player = player
        self.app_controller = app_controller
        self.current_queue: list[dict] = []
        self.current_index: int = -1
        self.shuffle_enabled = False
        self.repeat_enabled = False

        self.setWindowTitle(app_name)
        self.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        self.resize(window_width, window_height)

        self.sidebar_panel: Sidebar
        self.main_view_panel: LibraryView
        self.right_panel: NowPlayingPanel
        self.controls_panel: ControlsPanel

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.sidebar_panel = Sidebar()
        self.main_view_panel = LibraryView(self.database)
        self.right_panel = NowPlayingPanel()

        content_splitter.addWidget(self.sidebar_panel)
        content_splitter.addWidget(self.main_view_panel)
        content_splitter.addWidget(self.right_panel)

        content_splitter.setSizes([220, 800, 320])
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)
        content_splitter.setStretchFactor(2, 0)

        self.controls_panel = ControlsPanel()

        root_layout.addWidget(content_splitter, stretch=1)
        root_layout.addWidget(self.controls_panel, stretch=0)

    def _connect_signals(self) -> None:
        self.sidebar_panel.section_selected.connect(self._on_sidebar_section_selected)
        self.sidebar_panel.scan_folder_clicked.connect(self._on_scan_folder_clicked)

        self.main_view_panel.track_selected.connect(self._on_track_selected)

        self.controls_panel.play_clicked.connect(self._on_play_clicked)
        self.controls_panel.pause_clicked.connect(self._on_pause_clicked)
        self.controls_panel.next_clicked.connect(self._on_next_clicked)
        self.controls_panel.previous_clicked.connect(self._on_previous_clicked)
        self.controls_panel.shuffle_clicked.connect(self._on_shuffle_clicked)
        self.controls_panel.repeat_clicked.connect(self._on_repeat_clicked)
        self.controls_panel.volume_changed.connect(self._on_volume_changed)
        self.controls_panel.seek_changed.connect(self._on_seek_changed)

        self.player.position_changed.connect(self._on_player_position_changed)
        self.player.duration_changed.connect(self._on_player_duration_changed)
        self.player.media_status_changed.connect(self._on_media_status_changed)

    def _on_media_status_changed(self, status) -> None:
        from PySide6.QtMultimedia import QMediaPlayer

        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.shuffle_enabled:
                self._on_next_clicked()
            elif self.current_queue and self.current_index < len(self.current_queue) - 1:
                self._on_next_clicked()
            elif self.repeat_enabled:
                self._play_track_at_index(0)

    def _on_sidebar_section_selected(self, section_name: str) -> None:
        self.main_view_panel.show_section(section_name)

    def _on_scan_folder_clicked(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if not folder:
            return

        self.app_controller.add_music_folder(folder)
        scanned_count = self.scanner.scan([folder])

        current_section = "Home"
        for section_name, button in self.sidebar_panel.buttons().items():
            if button.isChecked():
                current_section = section_name
                break

        self.main_view_panel.show_section(current_section)
        self.right_panel.set_queue([f"Scanned {scanned_count} tracks from selected folder"])

    def _on_track_selected(self, track_data: dict) -> None:
        title = track_data.get("title", "Unknown Title")
        artist = track_data.get("artist_name", "Unknown Artist")
        album = track_data.get("album_title", "Unknown Album")
        file_path = track_data.get("file_path")

        self.current_queue = self.main_view_panel.get_current_track_list()

        self.current_index = -1
        for index, track in enumerate(self.current_queue):
            if track.get("file_path") == file_path:
                self.current_index = index
                break

        artwork_path = self._get_artwork_path_for_track(track_data)

        self.right_panel.set_now_playing(
            title=title,
            artist=artist,
            album=album,
            artwork_path=artwork_path,
        )

        queue_titles = [
            f'{track.get("title", "Unknown Title")} — {track.get("artist_name", "Unknown Artist")}'
            for track in self.current_queue[:25]
        ]
        self.right_panel.set_queue(queue_titles)

        self.controls_panel.set_now_playing(title=title, artist=artist)

        if file_path:
            self.player.play_track(file_path)

    def _on_play_clicked(self) -> None:
        self.player.play()

    def _on_pause_clicked(self) -> None:
        self.player.pause()

    def _on_shuffle_clicked(self) -> None:
        self.shuffle_enabled = self.controls_panel.shuffle_button.isChecked()

    def _on_repeat_clicked(self) -> None:
        self.repeat_enabled = self.controls_panel.repeat_button.isChecked()

    def _on_next_clicked(self) -> None:
        if not self.current_queue:
            return

        if self.shuffle_enabled and len(self.current_queue) > 1:
            possible_indexes = [i for i in range(len(self.current_queue)) if i != self.current_index]
            next_index = random.choice(possible_indexes)
        else:
            next_index = self.current_index + 1
            if next_index >= len(self.current_queue):
                if self.repeat_enabled:
                    next_index = 0
                else:
                    return

        self._play_track_at_index(next_index)

    def _on_previous_clicked(self) -> None:
        if not self.current_queue:
            return

        if self.shuffle_enabled and len(self.current_queue) > 1:
            possible_indexes = [i for i in range(len(self.current_queue)) if i != self.current_index]
            previous_index = random.choice(possible_indexes)
        else:
            previous_index = self.current_index - 1
            if previous_index < 0:
                if self.repeat_enabled:
                    previous_index = len(self.current_queue) - 1
                else:
                    return

        self._play_track_at_index(previous_index)

    def _on_volume_changed(self, value: int) -> None:
        self.player.set_volume(value)

    def _on_seek_changed(self, value: int) -> None:
        duration = self.player.get_duration()
        if duration > 0:
            position = int((value / 100) * duration)
            self.player.set_position(position)

    def _on_player_position_changed(self, position_ms: int) -> None:
        duration_ms = self.player.get_duration()

        if duration_ms > 0:
            progress = int((position_ms / duration_ms) * 100)
        else:
            progress = 0

        self.controls_panel.set_progress(progress, 100)
        self.controls_panel.set_time(
            f"{self._format_ms(position_ms)} / {self._format_ms(duration_ms)}"
        )

    def _on_player_duration_changed(self, duration_ms: int) -> None:
        position_ms = self.player.get_position()
        self.controls_panel.set_time(
            f"{self._format_ms(position_ms)} / {self._format_ms(duration_ms)}"
        )

    def _play_track_at_index(self, index: int) -> None:
        if not self.current_queue:
            return

        if not (0 <= index < len(self.current_queue)):
            return

        self.current_index = index
        track_data = self.current_queue[index]

        title = track_data.get("title", "Unknown Title")
        artist = track_data.get("artist_name", "Unknown Artist")
        album = track_data.get("album_title", "Unknown Album")
        file_path = track_data.get("file_path")

        artwork_path = self._get_artwork_path_for_track(track_data)

        self.right_panel.set_now_playing(
            title=title,
            artist=artist,
            album=album,
            artwork_path=artwork_path,
        )
        self.controls_panel.set_now_playing(title=title, artist=artist)

        if file_path:
            self.player.play_track(file_path)

    def _format_ms(self, milliseconds: int) -> str:        
        seconds = max(0, milliseconds // 1000)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02}"
    
    def _extract_album_art_to_cache(self, file_path: str) -> str | None:
        try:
            CACHE_DIR.mkdir(exist_ok=True)

            audio = MutagenFile(file_path)
            if audio is None:
                return None

            art_data = None
            extension = ".jpg"

            # MP3 / ID3 APIC
            if hasattr(audio, "tags") and audio.tags:
                if "APIC:" in audio.tags:
                    art_data = audio.tags["APIC:"].data
                    extension = ".jpg"
                else:
                    for tag in audio.tags.values():
                        if tag.__class__.__name__ == "APIC":
                            art_data = tag.data
                            extension = ".jpg"
                            break

            # FLAC
            if art_data is None and hasattr(audio, "pictures") and audio.pictures:
                art_data = audio.pictures[0].data
                mime = getattr(audio.pictures[0], "mime", "")
                extension = ".png" if "png" in mime.lower() else ".jpg"

            # MP4 / M4A
            if art_data is None and hasattr(audio, "tags") and audio.tags:
                covr = audio.tags.get("covr")
                if covr:
                    art_data = bytes(covr[0])
                    extension = ".jpg"

            if art_data is None:
                return None

            safe_name = Path(file_path).stem.replace(" ", "_")
            output_path = CACHE_DIR / f"{safe_name}_cover{extension}"

            with open(output_path, "wb") as image_file:
                image_file.write(art_data)

            return str(output_path)

        except Exception as exc:
            print(f"Failed to extract album art from {file_path}: {exc}")
            return None
        
    def _get_artwork_path_for_track(self, track_data: dict) -> str | None:
        file_path = track_data.get("file_path")
        if not file_path:
            return None

        return self._extract_album_art_to_cache(file_path)