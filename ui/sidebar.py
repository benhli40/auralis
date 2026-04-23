from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class Sidebar(QFrame):
    section_selected = Signal(str)
    scan_folder_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("sidebarPanel")
        self.setMinimumWidth(180)
        self.setMaximumWidth(260)

        self._buttons: dict[str, QPushButton] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Library")
        title.setObjectName("panelTitle")
        layout.addWidget(title)

        sections = [
            "Home",
            "Artists",
            "Albums",
            "Genres",
            "Songs",
            "Playlists",
        ]

        for section in sections:
            button = QPushButton(section)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.clicked.connect(lambda checked, name=section: self._handle_button_click(name))
            layout.addWidget(button)
            self._buttons[section] = button

        layout.addStretch()

        self.scan_button = QPushButton("Scan Folder")
        self.scan_button.setObjectName("scanFolderButton")
        self.scan_button.clicked.connect(self.scan_folder_clicked.emit)
        layout.addWidget(self.scan_button)

        self.set_active_section("Home")

    def _handle_button_click(self, section_name: str) -> None:
        self.set_active_section(section_name)
        self.section_selected.emit(section_name)

    def set_active_section(self, section_name: str) -> None:
        for name, button in self._buttons.items():
            button.setChecked(name == section_name)

    def buttons(self) -> dict[str, QPushButton]:
        return self._buttons