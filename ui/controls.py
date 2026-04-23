from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)


class ControlsPanel(QFrame):
    play_clicked = Signal()
    pause_clicked = Signal()
    next_clicked = Signal()
    previous_clicked = Signal()
    shuffle_clicked = Signal()
    repeat_clicked = Signal()
    seek_changed = Signal(int)
    volume_changed = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("controlsPanel")
        self.setMinimumHeight(120)
        self.setMaximumHeight(170)

        self.now_playing_label: QLabel
        self.time_label: QLabel
        self.progress_slider: QSlider
        self.volume_slider: QSlider

        self.shuffle_button: QPushButton
        self.prev_button: QPushButton
        self.play_button: QPushButton
        self.pause_button: QPushButton
        self.next_button: QPushButton
        self.repeat_button: QPushButton

        self._build_ui()
        self.set_now_playing()
        self.set_time("0:00 / 0:00")

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 16, 20, 16)
        root_layout.setSpacing(12)

        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        left_info = QWidget()
        left_layout = QVBoxLayout(left_info)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)

        self.now_playing_label = QLabel("Now Playing: Nothing")
        self.now_playing_label.setObjectName("nowPlayingLabel")

        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setObjectName("timeLabel")

        left_layout.addWidget(self.now_playing_label)
        left_layout.addWidget(self.time_label)

        controls_container = QWidget()
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)

        self.shuffle_button = QPushButton("🔀")
        self.prev_button = QPushButton("⏮")
        self.play_button = QPushButton("▶")
        self.pause_button = QPushButton("⏸")
        self.next_button = QPushButton("⏭")
        self.repeat_button = QPushButton("🔁")

        control_buttons = [
            self.shuffle_button,
            self.prev_button,
            self.play_button,
            self.pause_button,
            self.next_button,
            self.repeat_button,
        ]

        for button in control_buttons:
            button.setObjectName("transportButton")
            button.setMinimumSize(52, 52)
            button.setMaximumSize(52, 52)
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            if button in (self.shuffle_button, self.repeat_button):
                button.setCheckable(True)

            controls_layout.addWidget(button)

        self.shuffle_button.clicked.connect(self.shuffle_clicked.emit)
        self.prev_button.clicked.connect(self.previous_clicked.emit)
        self.play_button.clicked.connect(self.play_clicked.emit)
        self.pause_button.clicked.connect(self.pause_clicked.emit)
        self.next_button.clicked.connect(self.next_clicked.emit)
        self.repeat_button.clicked.connect(self.repeat_clicked.emit)

        volume_container = QWidget()
        volume_layout = QHBoxLayout(volume_container)
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setSpacing(8)

        volume_label = QLabel("Volume")

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(150)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)

        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)

        top_row.addWidget(left_info, stretch=1)
        top_row.addWidget(controls_container, stretch=0)
        top_row.addWidget(volume_container, stretch=0)

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(100)
        self.progress_slider.setValue(0)
        self.progress_slider.sliderMoved.connect(self.seek_changed.emit)

        root_layout.addLayout(top_row)
        root_layout.addWidget(self.progress_slider)

    def set_now_playing(self, title: str = "Nothing", artist: str = "") -> None:
        if artist:
            self.now_playing_label.setText(f"Now Playing: {title} — {artist}")
        else:
            self.now_playing_label.setText(f"Now Playing: {title}")

    def set_time(self, text: str) -> None:
        self.time_label.setText(text)

    def set_progress(self, value: int, maximum: int = 100) -> None:
        self.progress_slider.setMaximum(maximum)
        self.progress_slider.setValue(value)

    def set_volume(self, value: int) -> None:
        self.volume_slider.setValue(value)