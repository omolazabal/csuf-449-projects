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
    track_id GUID NOT NULL
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
    track_id GUID NOT NULL,
    user_name VARCHAR NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY(user_name) REFERENCES users(username) ON DELETE CASCADE,
    PRIMARY KEY(user_name)
);

COMMIT;

