from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QListWidget,
    QVBoxLayout,
)


class NowPlayingPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("rightPanel")
        self.setMinimumWidth(260)
        self.setMaximumWidth(420)

        self.album_art_label: QLabel
        self.track_title_label: QLabel
        self.artist_label: QLabel
        self.album_label: QLabel
        self.queue_list: QListWidget

        self._build_ui()
        self.set_now_playing()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("Now Playing")
        title.setObjectName("panelTitle")
        layout.addWidget(title)

        self.album_art_label = QLabel("No Album Art")
        self.album_art_label.setObjectName("albumArtLabel")
        self.album_art_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.album_art_label.setMinimumHeight(280)
        self.album_art_label.setFrameShape(QFrame.Shape.StyledPanel)
        layout.addWidget(self.album_art_label)

        self.track_title_label = QLabel("Nothing Playing")
        self.track_title_label.setObjectName("nowPlayingTrackTitle")
        self.track_title_label.setWordWrap(True)
        layout.addWidget(self.track_title_label)

        self.artist_label = QLabel("Artist")
        self.artist_label.setObjectName("nowPlayingArtist")
        self.artist_label.setWordWrap(True)
        layout.addWidget(self.artist_label)

        self.album_label = QLabel("Album")
        self.album_label.setObjectName("nowPlayingAlbum")
        self.album_label.setWordWrap(True)
        layout.addWidget(self.album_label)

        queue_title = QLabel("Queue")
        queue_title.setObjectName("panelTitle")
        layout.addWidget(queue_title)

        self.queue_list = QListWidget()
        layout.addWidget(self.queue_list, stretch=1)

    def set_now_playing(
        self,
        title: str = "Nothing Playing",
        artist: str = "Artist",
        album: str = "Album",
        artwork_path: str | None = None,
    ) -> None:
        self.track_title_label.setText(title)
        self.artist_label.setText(artist)
        self.album_label.setText(album)

        if artwork_path:
            pixmap = QPixmap(artwork_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    280,
                    280,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.album_art_label.setPixmap(scaled)
                self.album_art_label.setText("")
                return

        self.album_art_label.setPixmap(QPixmap())
        self.album_art_label.setText("No Album Art")

    def set_queue(self, tracks: list[str]) -> None:
        self.queue_list.clear()
        self.queue_list.addItems(tracks)