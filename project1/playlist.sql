-- $ sqlite3 playlist.db < sqlite.sql

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    title VARCHAR NOT NULL,
    album_title VARCHAR NOT NULL,
    time_len FLOAT NOT NULL,
    url_media_file TEXT NOT NULL,
    url_album_chart TEXT NULL

);

CREATE TABLE playlist(

    title VARCHAR NOT NULL,
    url_ind_tracks BLOB NOT NULL,
    username VARCHAR NOT NULL PRIMARY KEY,
    descript TEXT NULL,
    UNIQUE(username)

);

CREATE TABLE users(

    username VARCHAR NOT NULL PRIMARY KEY, 
    user_pass VARCHAR NOT NULL,
    disp_name VARCHAR NOT NULL ,
    url_homepage TEXT NULL,
    UNIQUE(username, disp_name)
);

CREATE TABLE microservice (

    user_description TEXT NULL,
    retrive_descipttion TEXT NULL
    


);