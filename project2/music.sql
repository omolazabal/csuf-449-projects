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
    media_file_url TEXT NOT NULL
    -- FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    -- FOREIGN KEY(media_file_url) REFERENCES tracks(media_file_url) ON DELETE CASCADE,
    -- PRIMARY KEY(playlist_id)
    
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
    track_id INTEGER NOT NULL,
    user_name VARCHAR NOT NULL,
    description TEXT NOT NULL,
    -- FOREIGN KEY(track_id) REFERENCES tracks(id) ON DELETE CASCADE,
    FOREIGN KEY(user_name) REFERENCES users(username) ON DELETE CASCADE,
    PRIMARY KEY(user_name)
);

COMMIT;

