-- $ sqlite3 music.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    id INTEGER primary key,
    title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    time_len FLOAT NOT NULL,
    url_media_file TEXT NOT NULL,
    url_album_chart TEXT NULL
);

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist(
    id INTEGER primary key,
    title VARCHAR NOT NULL,
    url_ind_tracks TEXT NOT NULL,
    username VARCHAR NOT NULL ,
    descript TEXT NULL
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

INSERT INTO tracks(title,album_title,time_len,url_media_file) VALUES("Parinod","Beerpng and Bentleys",2.23,"http://thisisawebsite.com");
INSERT INTO tracks(title,album_title,time_len,url_media_file) VALUES("Zack and Codine","Beerpng and Bentleys",2.55,"http://thisisawebsite2.com");
INSERT INTO playlist(title,url_ind_tracks,username) VALUES("Parinoid", "http://thisisawebsite.com","username1");
INSERT INTO playlist(title,url_ind_tracks,username) VALUES("Zack and Codine", "http://thisisawebsite.com2","username1");
INSERT INTO users(username,user_pass,disp_name,email,url_homepage) VALUES("username1","Password","username1","myemail@gmail.com","http://thisisaurl.com");
INSERT INTO descriptions(user_description) VALUES("This is a description");

COMMIT;

