-- $ sqlite3 music.db < sqlite.sql

PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    track_title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    track_length FLOAT NOT NULL,
    media_file_url TEXT NOT NULL,
    album_art_url TEXT NULL
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
    track_id INTEGER NOT NULL,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id),
    FOREIGN KEY(track_id) REFERENCES tracks(id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INTEGER primary key,
    username VARCHAR NOT NULL , 
    user_pass VARCHAR NOT NULL,
    disp_name VARCHAR NOT NULL ,
    email VARCHAR NOT NULL,
    url_homepage TEXT NULL,
    UNIQUE(username, disp_name)
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
    id INTEGER primary key,
    user_description TEXT NULL
);

INSERT INTO tracks(track_title, album_title, artist, track_length, media_file_url, album_art_url) VALUES("Track Title 1", "Album Title 1", "Artist 1", 2.3, "mediafileurl", "albumarturl");
INSERT INTO tracks(track_title, album_title, artist, track_length, media_file_url, album_art_url) VALUES("Track Title 2", "Album Title 2", "Artist 2", 3.3, "mediafileurl", "albumarturl");
INSERT INTO playlist(title,url_ind_tracks,username) VALUES("Parinoid", "http://thisisawebsite.com","username1");
INSERT INTO playlist(title,url_ind_tracks,username) VALUES("Zack and Codine", "http://thisisawebsite.com2","username1");
INSERT INTO users(username,user_pass,disp_name,email,url_homepage) VALUES("username1","Password","username1","myemail@gmail.com","http://thisisaurl.com");
INSERT INTO descriptions(user_description) VALUES("This is a description");

COMMIT;

