ACCENT_COLOR = "#5E81FF"
ACCENT_HOVER = "#7694FF"
ACCENT_PRESSED = "#4A6FE3"

BACKGROUND_MAIN = "#0B0F17"
BACKGROUND_PANEL = "#121826"
BACKGROUND_PANEL_ALT = "#161D2E"
BACKGROUND_HOVER = "#1B2438"

TEXT_PRIMARY = "#EAF1FF"
TEXT_SECONDARY = "#9FB0D0"
TEXT_MUTED = "#6F7D99"

BORDER_COLOR = "#24304A"
DIVIDER_COLOR = "#1E2740"

SUCCESS_COLOR = "#35C48B"
WARNING_COLOR = "#F0B35A"
DANGER_COLOR = "#E56B6F"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_BASE = "14px"
FONT_SIZE_SMALL = "12px"
FONT_SIZE_TITLE = "20px"


def get_stylesheet() -> str:
    return f"""
    QWidget {{
        background-color: {BACKGROUND_MAIN};
        color: {TEXT_PRIMARY};
        font-family: {FONT_FAMILY};
        font-size: {FONT_SIZE_BASE};
    }}

    QMainWindow {{
        background-color: {BACKGROUND_MAIN};
    }}

    QFrame#sidebarPanel,
    QFrame#mainViewPanel,
    QFrame#rightPanel,
    QFrame#controlsPanel {{
        background-color: {BACKGROUND_PANEL};
        border: 1px solid {BORDER_COLOR};
        border-radius: 16px;
    }}

    QFrame#artBox {{
        background-color: {BACKGROUND_PANEL_ALT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 18px;
    }}

    QLabel#panelTitle {{
        color: {TEXT_PRIMARY};
        font-size: {FONT_SIZE_TITLE};
        font-weight: 600;
        background: transparent;
        border: none;
    }}

    QLabel#nowPlayingLabel {{
        color: {TEXT_PRIMARY};
        font-size: 15px;
        font-weight: 500;
        background: transparent;
        border: none;
    }}

    QLabel#albumArtLabel {{
    background-color: {BACKGROUND_PANEL_ALT};
    border: 1px solid {BORDER_COLOR};
    border-radius: 18px;
    color: {TEXT_MUTED};
    font-size: 14px;
    padding: 12px;
    }}

    QLabel#nowPlayingTrackTitle {{
        color: {TEXT_PRIMARY};
        font-size: 18px;
        font-weight: 700;
        background: transparent;
        border: none;
    }}

    QLabel#nowPlayingArtist {{
        color: {TEXT_SECONDARY};
        font-size: 14px;
        font-weight: 500;
        background: transparent;
        border: none;
    }}

    QLabel#nowPlayingAlbum {{
        color: {TEXT_MUTED};
        font-size: 13px;
        background: transparent;
        border: none;
    }}

    QLabel {{
        background: transparent;
        border: none;
    }}

    QLabel#timeLabel {{
    color: {TEXT_MUTED};
    font-size: 13px;
    background: transparent;
    border: none;
    }}

    QPushButton {{
        background-color: {BACKGROUND_PANEL_ALT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 10px 14px;
        min-height: 18px;
    }}

    QPushButton#transportButton {{
        background-color: #161D2E;
        color: #EAF1FF;
        border: 1px solid #24304A;
        border-radius: 14px;
        font-size: 20px;
        font-weight: 600;
        padding: 0px;
    }}

    QPushButton#transportButton:hover {{
        background-color: #1B2438;
        border: 1px solid #5E81FF;
    }}

    QPushButton#transportButton:pressed {{
        background-color: #4A6FE3;
        border: 1px solid #4A6FE3;
        color: white;
    }}

    QPushButton#transportButton:checked {{
        background-color: #5E81FF;
        color: white;
        border: 2px solid #8FA8FF;
    }}

    QPushButton#scanFolderButton {{
    background-color: {ACCENT_COLOR};
    color: white;
    border: 1px solid {ACCENT_COLOR};
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 600;
    }}

    QPushButton#scanFolderButton:hover {{
        background-color: {ACCENT_HOVER};
        border: 1px solid {ACCENT_HOVER};
    }}

    QPushButton#scanFolderButton:pressed {{
        background-color: {ACCENT_PRESSED};
        border: 1px solid {ACCENT_PRESSED};
    }}

    QPushButton:hover {{
        background-color: {BACKGROUND_HOVER};
        border: 1px solid {ACCENT_COLOR};
    }}

    QPushButton:pressed {{
        background-color: {ACCENT_PRESSED};
        border: 1px solid {ACCENT_PRESSED};
        color: white;
    }}

    QPushButton:checked {{
        background-color: {ACCENT_COLOR};
        border: 1px solid {ACCENT_COLOR};
        color: white;
    }}

    QScrollArea {{
        background: transparent;
        border: none;
    }}

    QListWidget,
    QTreeWidget,
    QTableWidget {{
        background-color: {BACKGROUND_PANEL_ALT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 6px;
        gridline-color: {DIVIDER_COLOR};
        outline: none;
    }}

    QListWidget::item,
    QTreeWidget::item,
    QTableWidget::item {{
        padding: 8px;
        border-radius: 8px;
    }}

    QListWidget::item:selected,
    QTreeWidget::item:selected,
    QTableWidget::item:selected {{
        background-color: {ACCENT_COLOR};
        color: white;
    }}

    QListWidget::item:hover,
    QTreeWidget::item:hover,
    QTableWidget::item:hover {{
        background-color: {BACKGROUND_HOVER};
    }}

    QHeaderView::section {{
        background-color: {BACKGROUND_PANEL_ALT};
        color: {TEXT_SECONDARY};
        padding: 10px;
        border: none;
        border-bottom: 1px solid {BORDER_COLOR};
        font-weight: 600;
    }}

    QSplitter::handle {{
        background-color: {DIVIDER_COLOR};
    }}

    QSplitter::handle:horizontal {{
        width: 2px;
        margin: 8px 0;
    }}

    QSplitter::handle:vertical {{
        height: 2px;
        margin: 0 8px;
    }}

    QSlider::groove:horizontal {{
        border: none;
        height: 6px;
        background: {BACKGROUND_PANEL_ALT};
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        background: {ACCENT_COLOR};
        border: none;
        width: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }}

    QSlider::sub-page:horizontal {{
        background: {ACCENT_COLOR};
        border-radius: 3px;
    }}

    QLineEdit,
    QComboBox {{
        background-color: {BACKGROUND_PANEL_ALT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 10px;
        padding: 8px 10px;
    }}

    QLineEdit:focus,
    QComboBox:focus {{
        border: 1px solid {ACCENT_COLOR};
    }}
    """