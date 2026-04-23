from database import MusicDatabase
from scanner import MusicScanner

db = MusicDatabase()
db.initialize()

scanner = MusicScanner(db)
count = scanner.scan()

print(f"Scanned {count} tracks")

for track in db.get_all_tracks():
    print(
        track["artist_name"],
        "-",
        track["album_title"],
        "-",
        track["track_number"],
        "-",
        track["title"]
    )

db.close()