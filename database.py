import sqlite3
from pathlib import Path
from typing import Any

from config import DATABASE_PATH


class MusicDatabase:
    def __init__(self, db_path: Path | str = DATABASE_PATH) -> None:
        self.db_path = str(db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def initialize(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                year TEXT,
                artwork_path TEXT,
                UNIQUE(title, artist_id),
                FOREIGN KEY (artist_id) REFERENCES artists(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                album_id INTEGER NOT NULL,
                genre_id INTEGER,
                track_number INTEGER,
                duration INTEGER,
                file_path TEXT NOT NULL UNIQUE,
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (album_id) REFERENCES albums(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id)
            )
        """)

        self.connection.commit()

    def get_or_create_artist(self, name: str) -> int:
        self.cursor.execute("SELECT id FROM artists WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        if row:
            return int(row["id"])

        self.cursor.execute("INSERT INTO artists (name) VALUES (?)", (name,))
        self.connection.commit()
        return int(self.cursor.lastrowid)
    
    def rename_artist_by_id(self, artist_id: int, new_name: str) -> None:
        new_name = new_name.strip()
        if not new_name:
            return

        self.cursor.execute(
            "UPDATE artists SET name = ? WHERE id = ?",
            (new_name, artist_id),
        )
        self.connection.commit()

    def get_or_create_album(self, title: str, artist_id: int, year: str | None = None) -> int:
        self.cursor.execute(
            "SELECT id FROM albums WHERE title = ? AND artist_id = ?",
            (title, artist_id),
        )
        row = self.cursor.fetchone()
        if row:
            return int(row["id"])

        self.cursor.execute(
            "INSERT INTO albums (title, artist_id, year) VALUES (?, ?, ?)",
            (title, artist_id, year),
        )
        self.connection.commit()
        return int(self.cursor.lastrowid)

    def get_or_create_genre(self, name: str) -> int:
        self.cursor.execute("SELECT id FROM genres WHERE name = ?", (name,))
        row = self.cursor.fetchone()
        if row:
            return int(row["id"])

        self.cursor.execute("INSERT INTO genres (name) VALUES (?)", (name,))
        self.connection.commit()
        return int(self.cursor.lastrowid)
    
    def get_tracks_by_artist(self, artist_id: int) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT id, file_path
            FROM tracks
            WHERE artist_id = ?
            ORDER BY file_path COLLATE NOCASE
        """, (artist_id,))
        return list(self.cursor.fetchall())
    
    def get_artist_by_id(self, artist_id: int) -> sqlite3.Row | None:
        self.cursor.execute(
            "SELECT id, name FROM artists WHERE id = ?",
            (artist_id,),
        )
        return self.cursor.fetchone()

    def get_album_by_id(self, album_id: int) -> sqlite3.Row | None:
        self.cursor.execute("""
            SELECT albums.id, albums.title, artists.name AS artist_name, albums.year
            FROM albums
            JOIN artists ON albums.artist_id = artists.id
            WHERE albums.id = ?
        """, (album_id,))
        return self.cursor.fetchone()

    def get_genre_by_id(self, genre_id: int) -> sqlite3.Row | None:
        self.cursor.execute(
            "SELECT id, name FROM genres WHERE id = ?",
            (genre_id,),
        )
        return self.cursor.fetchone()

    def rename_genre_by_id(self, genre_id: int, new_name: str) -> None:
        new_name = new_name.strip()
        if not new_name:
            return

        self.cursor.execute(
            "UPDATE genres SET name = ? WHERE id = ?",
            (new_name, genre_id),
        )
        self.connection.commit()

    def add_or_update_track(
        self,
        title: str,
        artist_name: str,
        album_title: str,
        genre_name: str | None,
        track_number: int | None,
        duration: int | None,
        file_path: str,
        year: str | None = None,
    ) -> None:
        artist_id = self.get_or_create_artist(artist_name)
        album_id = self.get_or_create_album(album_title, artist_id, year)

        genre_id = None
        if genre_name:
            genre_id = self.get_or_create_genre(genre_name)

        self.cursor.execute("SELECT id FROM tracks WHERE file_path = ?", (file_path,))
        existing = self.cursor.fetchone()

        if existing:
            self.cursor.execute("""
                UPDATE tracks
                SET title = ?,
                    artist_id = ?,
                    album_id = ?,
                    genre_id = ?,
                    track_number = ?,
                    duration = ?
                WHERE file_path = ?
            """, (
                title,
                artist_id,
                album_id,
                genre_id,
                track_number,
                duration,
                file_path,
            ))
        else:
            self.cursor.execute("""
                INSERT INTO tracks (
                    title,
                    artist_id,
                    album_id,
                    genre_id,
                    track_number,
                    duration,
                    file_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                artist_id,
                album_id,
                genre_id,
                track_number,
                duration,
                file_path,
            ))

        self.connection.commit()

    def get_all_artists(self) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT id, name
            FROM artists
            ORDER BY name COLLATE NOCASE
        """)
        return list(self.cursor.fetchall())

    def get_all_albums(self) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT albums.id, albums.title, artists.name AS artist_name, albums.year, albums.artwork_path
            FROM albums
            JOIN artists ON albums.artist_id = artists.id
            ORDER BY artists.name COLLATE NOCASE, albums.title COLLATE NOCASE
        """)
        return list(self.cursor.fetchall())

    def get_all_genres(self) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT id, name
            FROM genres
            ORDER BY name COLLATE NOCASE
        """)
        return list(self.cursor.fetchall())

    def get_all_tracks(self) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT
                tracks.id,
                tracks.title,
                artists.name AS artist_name,
                albums.title AS album_title,
                genres.name AS genre_name,
                tracks.track_number,
                tracks.duration,
                tracks.file_path
            FROM tracks
            JOIN artists ON tracks.artist_id = artists.id
            JOIN albums ON tracks.album_id = albums.id
            LEFT JOIN genres ON tracks.genre_id = genres.id
            ORDER BY artists.name COLLATE NOCASE,
                     albums.title COLLATE NOCASE,
                     tracks.track_number,
                     tracks.title COLLATE NOCASE
        """)
        return list(self.cursor.fetchall())

    def get_tracks_by_artist(self, artist_id: int) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT
                tracks.id,
                tracks.title,
                albums.title AS album_title,
                genres.name AS genre_name,
                tracks.track_number,
                tracks.duration,
                tracks.file_path
            FROM tracks
            JOIN albums ON tracks.album_id = albums.id
            LEFT JOIN genres ON tracks.genre_id = genres.id
            WHERE tracks.artist_id = ?
            ORDER BY albums.title COLLATE NOCASE,
                     tracks.track_number,
                     tracks.title COLLATE NOCASE
        """, (artist_id,))
        return list(self.cursor.fetchall())

    def get_tracks_by_album(self, album_id: int) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT
                tracks.id,
                tracks.title,
                artists.name AS artist_name,
                genres.name AS genre_name,
                tracks.track_number,
                tracks.duration,
                tracks.file_path
            FROM tracks
            JOIN artists ON tracks.artist_id = artists.id
            LEFT JOIN genres ON tracks.genre_id = genres.id
            WHERE tracks.album_id = ?
            ORDER BY tracks.track_number, tracks.title COLLATE NOCASE
        """, (album_id,))
        return list(self.cursor.fetchall())

    def get_tracks_by_genre(self, genre_id: int) -> list[sqlite3.Row]:
        self.cursor.execute("""
            SELECT
                tracks.id,
                tracks.title,
                artists.name AS artist_name,
                albums.title AS album_title,
                tracks.track_number,
                tracks.duration,
                tracks.file_path
            FROM tracks
            JOIN artists ON tracks.artist_id = artists.id
            JOIN albums ON tracks.album_id = albums.id
            WHERE tracks.genre_id = ?
            ORDER BY artists.name COLLATE NOCASE,
                     albums.title COLLATE NOCASE,
                     tracks.track_number,
                     tracks.title COLLATE NOCASE
        """, (genre_id,))
        return list(self.cursor.fetchall())

    def remove_missing_tracks(self) -> None:
        self.cursor.execute("SELECT id, file_path FROM tracks")
        rows = self.cursor.fetchall()

        missing_track_ids = []
        for row in rows:
            file_path = row["file_path"]
            if not Path(file_path).exists():
                missing_track_ids.append(int(row["id"]))

        for track_id in missing_track_ids:
            self.cursor.execute("DELETE FROM tracks WHERE id = ?", (track_id,))

        self.connection.commit()