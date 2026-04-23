from pathlib import Path
from typing import Iterable

from mutagen import File as MutagenFile

from config import (
    DEFAULT_MUSIC_FOLDERS,
    SUPPORTED_AUDIO_EXTENSIONS,
    UNKNOWN_ALBUM,
    UNKNOWN_ARTIST,
    UNKNOWN_GENRE,
    UNKNOWN_TITLE,
)
from database import MusicDatabase


class MusicScanner:
    def __init__(self, database: MusicDatabase) -> None:
        self.database = database

    def scan(self, folders: Iterable[Path] | None = None) -> int:
        folders_to_scan = list(folders) if folders is not None else DEFAULT_MUSIC_FOLDERS
        scanned_count = 0

        for folder in folders_to_scan:
            folder_path = Path(folder)
            if not folder_path.exists() or not folder_path.is_dir():
                continue

            for file_path in folder_path.rglob("*"):
                if not file_path.is_file():
                    continue

                if file_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
                    continue

                metadata = self.extract_metadata(file_path)
                self.database.add_or_update_track(
                    title=metadata["title"],
                    artist_name=metadata["artist"],
                    album_title=metadata["album"],
                    genre_name=metadata["genre"],
                    track_number=metadata["track_number"],
                    duration=metadata["duration"],
                    file_path=str(file_path),
                    year=metadata["year"],
                )
                scanned_count += 1

        self.database.remove_missing_tracks()
        return scanned_count

    def extract_metadata(self, file_path: Path) -> dict[str, str | int | None]:
        title = UNKNOWN_TITLE
        artist = UNKNOWN_ARTIST
        album = UNKNOWN_ALBUM
        genre = UNKNOWN_GENRE
        track_number = None
        duration = None
        year = None

        try:
            audio = MutagenFile(file_path, easy=True)

            if audio is not None:
                title = self._first_tag(audio, "title", fallback=file_path.stem)
                artist = self._first_tag(audio, "artist", fallback=UNKNOWN_ARTIST)
                album = self._first_tag(audio, "album", fallback=UNKNOWN_ALBUM)
                genre = self._first_tag(audio, "genre", fallback=UNKNOWN_GENRE)
                year = self._first_tag(audio, "date", fallback=None)

                raw_track = self._first_tag(audio, "tracknumber", fallback=None)
                track_number = self._parse_track_number(raw_track)

                if hasattr(audio, "info") and audio.info is not None:
                    if hasattr(audio.info, "length"):
                        duration = int(audio.info.length)

        except Exception:
            # For now, fail quietly and fall back to defaults.
            # Later you may want logging here.
            pass

        return {
            "title": title or file_path.stem,
            "artist": artist or UNKNOWN_ARTIST,
            "album": album or UNKNOWN_ALBUM,
            "genre": genre or UNKNOWN_GENRE,
            "track_number": track_number,
            "duration": duration,
            "year": year,
        }

    def _first_tag(self, audio: object, key: str, fallback: str | None = None) -> str | None:
        try:
            value = audio.get(key, [fallback])  # type: ignore[attr-defined]
            if isinstance(value, list) and value:
                return str(value[0]).strip() if value[0] is not None else fallback
            if value is not None:
                return str(value).strip()
        except Exception:
            pass
        return fallback

    def _parse_track_number(self, raw_value: str | None) -> int | None:
        if not raw_value:
            return None

        track_text = str(raw_value).split("/")[0].strip()
        if track_text.isdigit():
            return int(track_text)

        return None