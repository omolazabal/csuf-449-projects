-- $ sqlite3 music.db < sqlite.sql

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INTEGER primary key,
    username VARCHAR NOT NULL , 
    user_pass VARCHAR NOT NULL,
    disp_name VARCHAR NOT NULL ,
    email VARCHAR NOT NULL,
    url_homepage TEXT NULL,
    UNIQUE(username),
    UNIQUE(disp_name)
);

DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    track_title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    track_length FLOAT NOT NULL,
    media_file_url TEXT NOT NULL,
    album_art_url TEXT NULL,
    UNIQUE(media_file_url),
    UNIQUE(album_art_url)
);

DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists(
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    creator VARCHAR NOT NULL, 
    description TEXT NULL,
    FOREIGN KEY(creator) REFERENCES users(username)
);

DROP TABLE IF EXISTS playlist_tracks;
CREATE TABLE playlist_tracks(
    playlist_id INTEGER NOT NULL,
    media_file_url TEXT NOT NULL,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY(media_file_url) REFERENCES tracks(media_file_url),
    PRIMARY KEY(playlist_id, media_file_url)
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
    id INTEGER primary key,
    user_description TEXT NULL
);

COMMIT;

