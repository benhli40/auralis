from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class AudioPlayer(QObject):
    track_changed = Signal(str)
    playback_state_changed = Signal(object)
    position_changed = Signal(int)
    duration_changed = Signal(int)
    media_status_changed = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.70)

        self.current_track_path: str | None = None

        self.media_player.playbackStateChanged.connect(self.playback_state_changed.emit)
        self.media_player.positionChanged.connect(self.position_changed.emit)
        self.media_player.durationChanged.connect(self.duration_changed.emit)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed.emit)

    def load_track(self, file_path: str) -> None:
        path = Path(file_path)
        if not path.exists():
            return

        self.current_track_path = str(path)
        self.media_player.setSource(QUrl.fromLocalFile(str(path)))
        self.track_changed.emit(str(path))

    def play(self) -> None:
        self.media_player.play()

    def pause(self) -> None:
        self.media_player.pause()

    def stop(self) -> None:
        self.media_player.stop()

    def play_track(self, file_path: str) -> None:
        self.load_track(file_path)
        self.play()

    def set_volume(self, value: int) -> None:
        value = max(0, min(100, value))
        self.audio_output.setVolume(value / 100)

    def set_position(self, position_ms: int) -> None:
        self.media_player.setPosition(max(0, position_ms))

    def get_position(self) -> int:
        return self.media_player.position()

    def get_duration(self) -> int:
        return self.media_player.duration()

    def is_playing(self) -> bool:
        return self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def is_paused(self) -> bool:
        return self.media_player.playbackState() == QMediaPlayer.PlaybackState.PausedState

    def has_media(self) -> bool:
        return self.current_track_path is not None