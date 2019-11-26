DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    uuid  GUID PRIMARY KEY,
    track_title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    track_length FLOAT NOT NULL,
    media_file_url TEXT NOT NULL,
    album_art_url TEXT NULL,
    UNIQUE(media_file_url),
    UNIQUE(album_art_url)
);