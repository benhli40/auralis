from mutagen import File as MutagenFile

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class LibraryView(QFrame):
    track_selected = Signal(dict)

    def __init__(self, database) -> None:
        super().__init__()

        self.database = database
        self.current_track_context: list[dict] = []
        self.setObjectName("mainViewPanel")

        self.stack = QStackedWidget()

        self.home_page = self._build_home_page()
        self.artists_page = self._build_artists_page()
        self.albums_page = self._build_albums_page()
        self.genres_page = self._build_genres_page()
        self.songs_page = self._build_songs_page()
        self.playlists_page = self._build_placeholder_page(
            "Playlists",
            "Playlist support is coming next."
        )
        
        self.artist_detail_page = self._build_artist_detail_page()
        self.album_detail_page = self._build_album_detail_page()
        self.genre_detail_page = self._build_genre_detail_page()
        self.current_genre_id = None

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.artists_page)
        self.stack.addWidget(self.albums_page)
        self.stack.addWidget(self.genres_page)
        self.stack.addWidget(self.songs_page)
        self.stack.addWidget(self.artist_detail_page)
        self.stack.addWidget(self.album_detail_page)
        self.stack.addWidget(self.genre_detail_page)
        self.stack.addWidget(self.playlists_page)
        self.stack.addWidget(self.artist_detail_page)
        self.stack.addWidget(self.album_detail_page)
        self.stack.addWidget(self.genre_detail_page)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(self.stack)

        self.show_section("Home")

    def show_section(self, section_name: str) -> None:
        page_map = {
            "Home": self.home_page,
            "Artists": self.artists_page,
            "Albums": self.albums_page,
            "Genres": self.genres_page,
            "Songs": self.songs_page,
            "Playlists": self.playlists_page,
        }

        page = page_map.get(section_name, self.home_page)
        self.stack.setCurrentWidget(page)

        if section_name == "Home":
            self.refresh_home()
        elif section_name == "Artists":
            self.refresh_artists()
        elif section_name == "Albums":
            self.refresh_albums()
        elif section_name == "Genres":
            self.refresh_genres()
        elif section_name == "Songs":
            self.refresh_songs()

    def _build_home_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Home")
        title.setObjectName("panelTitle")

        subtitle = QLabel("Your modern music library, all in one place.")
        subtitle.setWordWrap(True)

        self.home_stats_label = QLabel("Loading library stats...")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.home_stats_label)
        layout.addStretch()

        return page

    def _build_artists_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setSpacing(10)

        title = QLabel("Artists")
        title.setObjectName("panelTitle")

        self.rename_artist_button = QPushButton("Rename Artist")
        self.rename_artist_button.clicked.connect(self._rename_selected_artist)

        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(self.rename_artist_button)

        self.artists_list = QListWidget()
        self.artists_list.itemDoubleClicked.connect(self._open_selected_artist)

        layout.addLayout(header_row)
        layout.addWidget(self.artists_list)

        return page
    
    def _build_artist_detail_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        self.artist_detail_title = QLabel("Artist")
        self.artist_detail_title.setObjectName("panelTitle")

        self.back_from_artist_button = QPushButton("Back")
        self.back_from_artist_button.clicked.connect(lambda: self.show_section("Artists"))

        header_row.addWidget(self.artist_detail_title)
        header_row.addStretch()
        header_row.addWidget(self.back_from_artist_button)

        self.artist_tracks_table = QTableWidget()
        self.artist_tracks_table.setColumnCount(4)
        self.artist_tracks_table.setHorizontalHeaderLabels(["Track", "Title", "Album", "Duration"])
        self.artist_tracks_table.verticalHeader().setVisible(False)
        self.artist_tracks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.artist_tracks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.artist_tracks_table.cellDoubleClicked.connect(self._handle_artist_track_double_click)

        layout.addLayout(header_row)
        layout.addWidget(self.artist_tracks_table)
        return page
    
    def _build_album_detail_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        self.album_detail_title = QLabel("Album")
        self.album_detail_title.setObjectName("panelTitle")

        self.back_from_album_button = QPushButton("Back")
        self.back_from_album_button.clicked.connect(lambda: self.show_section("Albums"))

        header_row.addWidget(self.album_detail_title)
        header_row.addStretch()
        header_row.addWidget(self.back_from_album_button)

        self.album_tracks_table = QTableWidget()
        self.album_tracks_table.setColumnCount(4)
        self.album_tracks_table.setHorizontalHeaderLabels(["Track", "Title", "Artist", "Duration"])
        self.album_tracks_table.verticalHeader().setVisible(False)
        self.album_tracks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.album_tracks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.album_tracks_table.cellDoubleClicked.connect(self._handle_album_track_double_click)

        layout.addLayout(header_row)
        layout.addWidget(self.album_tracks_table)
        return page

    def _build_genre_detail_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        header_row = QHBoxLayout()
        self.genre_detail_title = QLabel("Genre")
        self.genre_detail_title.setObjectName("panelTitle")

        self.rename_genre_button = QPushButton("Rename Genre")
        self.rename_genre_button.clicked.connect(self._rename_selected_genre_detail)

        self.back_from_genre_button = QPushButton("Back")
        self.back_from_genre_button.clicked.connect(lambda: self.show_section("Genres"))

        header_row.addWidget(self.genre_detail_title)
        header_row.addStretch()
        header_row.addWidget(self.rename_genre_button)
        header_row.addWidget(self.back_from_genre_button)

        self.genre_tracks_table = QTableWidget()
        self.genre_tracks_table.setColumnCount(4)
        self.genre_tracks_table.setHorizontalHeaderLabels(["Track", "Title", "Artist", "Album"])
        self.genre_tracks_table.verticalHeader().setVisible(False)
        self.genre_tracks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.genre_tracks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.genre_tracks_table.cellDoubleClicked.connect(self._handle_genre_track_double_click)

        layout.addLayout(header_row)
        layout.addWidget(self.genre_tracks_table)
        return page

    def _build_albums_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Albums")
        title.setObjectName("panelTitle")

        self.albums_table = QTableWidget()
        self.albums_table.setColumnCount(3)
        self.albums_table.setHorizontalHeaderLabels(["Album", "Artist", "Year"])
        self.albums_table.verticalHeader().setVisible(False)
        self.albums_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.albums_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.albums_table.cellDoubleClicked.connect(self._open_selected_album)

        layout.addWidget(title)
        layout.addWidget(self.albums_table)

        return page

    def _build_genres_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Genres")
        title.setObjectName("panelTitle")

        self.genres_list = QListWidget()
        self.genres_list.itemDoubleClicked.connect(self._open_selected_genre)

        layout.addWidget(title)
        layout.addWidget(self.genres_list)

        return page

    def _build_songs_page(self) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("Songs")
        title.setObjectName("panelTitle")

        self.songs_table = QTableWidget()
        self.songs_table.setColumnCount(5)
        self.songs_table.setHorizontalHeaderLabels(
            ["Track", "Title", "Artist", "Album", "Duration"]
        )
        self.songs_table.verticalHeader().setVisible(False)
        self.songs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.songs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.songs_table.cellDoubleClicked.connect(self._handle_song_double_click)

        layout.addWidget(title)
        layout.addWidget(self.songs_table)

        return page

    def _build_placeholder_page(self, title_text: str, body_text: str) -> QFrame:
        page = QFrame()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel(title_text)
        title.setObjectName("panelTitle")

        body = QLabel(body_text)
        body.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(body)
        layout.addStretch()

        return page

    def refresh_home(self) -> None:
        artist_count = len(self.database.get_all_artists())
        album_count = len(self.database.get_all_albums())
        genre_count = len(self.database.get_all_genres())
        track_count = len(self.database.get_all_tracks())

        self.home_stats_label.setText(
            f"Artists: {artist_count}    Albums: {album_count}    "
            f"Genres: {genre_count}    Tracks: {track_count}"
        )

    def refresh_artists(self) -> None:
        self.artists_list.clear()

        for artist in self.database.get_all_artists():
            item = QListWidgetItem(artist["name"])
            item.setData(Qt.ItemDataRole.UserRole, artist["id"])
            self.artists_list.addItem(item)

    def _write_artist_to_file_tags(self, file_path: str, new_name: str) -> None:

    
        try:
            audio = MutagenFile(file_path, easy=True)
            if audio is None:
                return

            audio["artist"] = [new_name]
            audio.save()
        except Exception as exc:
            print(f"Failed to update tags for {file_path}: {exc}")

    def _write_genre_to_file_tags(self, file_path: str, new_name: str) -> None:
        try:
            audio = MutagenFile(file_path, easy=True)
            if audio is None:
                return

            audio["genre"] = [new_name]
            audio.save()
        except Exception as exc:
            print(f"Failed to update genre tags for {file_path}: {exc}")

    def _rename_selected_artist(self) -> None:
        current_item = self.artists_list.currentItem()
        if current_item is None:
            return

        artist_id = current_item.data(Qt.ItemDataRole.UserRole)
        current_name = current_item.text()

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Artist",
            "Enter new artist name:",
            text=current_name,
        )

        if not ok:
            return

        new_name = new_name.strip()
        if not new_name or new_name == current_name:
            return

        tracks = self.database.get_tracks_by_artist(int(artist_id))

        for track in tracks:
            file_path = track["file_path"]
            self._write_artist_to_file_tags(file_path, new_name)

        self.database.rename_artist_by_id(int(artist_id), new_name)

        self.refresh_artists()
        self.refresh_albums()
        self.refresh_songs()
        self.refresh_home()

    def _rename_selected_genre_detail(self) -> None:
        genre_id = self.current_genre_id
        if genre_id is None:
            return

        current_name = self.genre_detail_title.text()

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Genre",
            "Enter new genre name:",
            text=current_name,
        )

        if not ok:
            return

        new_name = new_name.strip()
        if not new_name or new_name == current_name:
            return

        tracks = self.database.get_tracks_by_genre(int(genre_id))

        for track in tracks:
            file_path = track["file_path"]
            self._write_genre_to_file_tags(file_path, new_name)

        self.database.rename_genre_by_id(int(genre_id), new_name)

        self.genre_detail_title.setText(new_name)
        self.refresh_genres()
        self.refresh_songs()
        self.refresh_home()

    def refresh_albums(self) -> None:
        albums = self.database.get_all_albums()
        self.albums_table.setRowCount(len(albums))

        for row, album in enumerate(albums):
            album_data = dict(album)

            album_item = QTableWidgetItem(album["title"])
            artist_item = QTableWidgetItem(album["artist_name"])
            year_item = QTableWidgetItem(album["year"] or "")

            album_item.setData(Qt.ItemDataRole.UserRole, album_data)
            artist_item.setData(Qt.ItemDataRole.UserRole, album_data)
            year_item.setData(Qt.ItemDataRole.UserRole, album_data)

            self.albums_table.setItem(row, 0, album_item)
            self.albums_table.setItem(row, 1, artist_item)
            self.albums_table.setItem(row, 2, year_item)

        self.albums_table.resizeColumnsToContents()
        self.albums_table.horizontalHeader().setStretchLastSection(True)

    def refresh_genres(self) -> None:
        self.genres_list.clear()

        for genre in self.database.get_all_genres():
            item = QListWidgetItem(genre["name"])
            item.setData(Qt.ItemDataRole.UserRole, genre["id"])
            self.genres_list.addItem(item)

    def refresh_songs(self) -> None:
        tracks = self.database.get_all_tracks()
        self.current_track_context = [dict(track) for track in tracks]
        self.songs_table.setRowCount(len(tracks))

        for row, track in enumerate(tracks):
            track_number = "" if track["track_number"] is None else str(track["track_number"])
            duration = self._format_duration(track["duration"])

            self.songs_table.setItem(row, 0, QTableWidgetItem(track_number))
            self.songs_table.setItem(row, 1, QTableWidgetItem(track["title"]))
            self.songs_table.setItem(row, 2, QTableWidgetItem(track["artist_name"]))
            self.songs_table.setItem(row, 3, QTableWidgetItem(track["album_title"]))
            self.songs_table.setItem(row, 4, QTableWidgetItem(duration))

            self.songs_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, dict(track))
            self.songs_table.item(row, 1).setData(Qt.ItemDataRole.UserRole, dict(track))
            self.songs_table.item(row, 2).setData(Qt.ItemDataRole.UserRole, dict(track))
            self.songs_table.item(row, 3).setData(Qt.ItemDataRole.UserRole, dict(track))
            self.songs_table.item(row, 4).setData(Qt.ItemDataRole.UserRole, dict(track))

        self.songs_table.resizeColumnsToContents()
        self.songs_table.horizontalHeader().setStretchLastSection(True)

    def _open_selected_artist(self, item: QListWidgetItem) -> None:
        artist_id = item.data(Qt.ItemDataRole.UserRole)
        artist = self.database.get_artist_by_id(int(artist_id))
        if artist is None:
            return

        self.artist_detail_title.setText(artist["name"])
        tracks = self.database.get_tracks_by_artist(int(artist_id))
        self._populate_artist_tracks_table(tracks)
        self.stack.setCurrentWidget(self.artist_detail_page)


    def _open_selected_album(self, row: int, column: int) -> None:
        item = self.albums_table.item(row, column)
        if item is None:
            return

        album_data = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(album_data, dict):
            return

        album_id = int(album_data["id"])
        album = self.database.get_album_by_id(album_id)
        if album is None:
            return

        self.album_detail_title.setText(f'{album["title"]} — {album["artist_name"]}')
        tracks = self.database.get_tracks_by_album(album_id)
        self._populate_album_tracks_table(tracks)
        self.stack.setCurrentWidget(self.album_detail_page)


    def _open_selected_genre(self, item: QListWidgetItem) -> None:
        genre_id = item.data(Qt.ItemDataRole.UserRole)
        genre = self.database.get_genre_by_id(int(genre_id))
        if genre is None:
            return

        self.current_genre_id = int(genre_id)
        self.genre_detail_title.setText(genre["name"])

        tracks = self.database.get_tracks_by_genre(int(genre_id))
        self._populate_genre_tracks_table(tracks)

        self.stack.setCurrentWidget(self.genre_detail_page)


    def _populate_artist_tracks_table(self, tracks) -> None:
        self.current_track_context = [dict(track) for track in tracks]
        self.artist_tracks_table.setRowCount(len(tracks))

        for row, track in enumerate(tracks):
            track_number = "" if track["track_number"] is None else str(track["track_number"])
            duration = self._format_duration(track["duration"])

            items = [
                QTableWidgetItem(track_number),
                QTableWidgetItem(track["title"]),
                QTableWidgetItem(track["album_title"]),
                QTableWidgetItem(duration),
            ]

            for col, table_item in enumerate(items):
                table_item.setData(Qt.ItemDataRole.UserRole, dict(track))
                self.artist_tracks_table.setItem(row, col, table_item)

        self.artist_tracks_table.resizeColumnsToContents()
        self.artist_tracks_table.horizontalHeader().setStretchLastSection(True)


    def _populate_album_tracks_table(self, tracks) -> None:
        self.album_tracks_table.setRowCount(len(tracks))

        for row, track in enumerate(tracks):
            track_number = "" if track["track_number"] is None else str(track["track_number"])
            duration = self._format_duration(track["duration"])

            items = [
                QTableWidgetItem(track_number),
                QTableWidgetItem(track["title"]),
                QTableWidgetItem(track["artist_name"]),
                QTableWidgetItem(duration),
            ]

            for col, table_item in enumerate(items):
                table_item.setData(Qt.ItemDataRole.UserRole, dict(track))
                self.album_tracks_table.setItem(row, col, table_item)

        self.album_tracks_table.resizeColumnsToContents()
        self.album_tracks_table.horizontalHeader().setStretchLastSection(True)


    def _populate_genre_tracks_table(self, tracks) -> None:
        self.genre_tracks_table.setRowCount(len(tracks))

        for row, track in enumerate(tracks):
            track_number = "" if track["track_number"] is None else str(track["track_number"])

            items = [
                QTableWidgetItem(track_number),
                QTableWidgetItem(track["title"]),
                QTableWidgetItem(track["artist_name"]),
                QTableWidgetItem(track["album_title"]),
            ]

            for col, table_item in enumerate(items):
                table_item.setData(Qt.ItemDataRole.UserRole, dict(track))
                self.genre_tracks_table.setItem(row, col, table_item)

        self.genre_tracks_table.resizeColumnsToContents()
        self.genre_tracks_table.horizontalHeader().setStretchLastSection(True)


    def _handle_artist_track_double_click(self, row: int, column: int) -> None:
        item = self.artist_tracks_table.item(row, column)
        if item is not None:
            track_data = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(track_data, dict):
                self.track_selected.emit(track_data)


    def _handle_album_track_double_click(self, row: int, column: int) -> None:
        item = self.album_tracks_table.item(row, column)
        if item is not None:
            track_data = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(track_data, dict):
                self.track_selected.emit(track_data)


    def _handle_genre_track_double_click(self, row: int, column: int) -> None:
        item = self.genre_tracks_table.item(row, column)
        if item is not None:
            track_data = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(track_data, dict):
                self.track_selected.emit(track_data)


    def _rename_selected_genre_detail(self) -> None:
        genre_id = self.current_genre_id
        if genre_id is None:
            return

        current_name = self.genre_detail_title.text()

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Genre",
            "Enter new genre name:",
            text=current_name,
        )

        if not ok:
            return

        new_name = new_name.strip()
        if not new_name or new_name == current_name:
            return

        tracks = self.database.get_tracks_by_genre(int(genre_id))

        for track in tracks:
            file_path = track["file_path"]
            self._write_genre_to_file_tags(file_path, new_name)

        self.database.rename_genre_by_id(int(genre_id), new_name)

        self.genre_detail_title.setText(new_name)

        updated_tracks = self.database.get_tracks_by_genre(int(genre_id))
        self._populate_genre_tracks_table(updated_tracks)

        self.refresh_genres()
        self.refresh_songs()
        self.refresh_home()

    def _handle_song_double_click(self, row: int, column: int) -> None:
        item = self.songs_table.item(row, column)
        if item is None:
            return

        track_data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(track_data, dict):
            self.track_selected.emit(track_data)

    def _format_duration(self, seconds: int | None) -> str:
        if seconds is None:
            return ""

        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02}"
    
    def get_current_track_list(self) -> list[dict]:
        return list(self.current_track_context)